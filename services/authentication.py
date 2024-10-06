import os

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from services.users_database import create_user, user_already_exists, get_user_by_username, is_user_admin_or_owner, get_user_role_name
from config.roles import role_configurations

from models.user_in_db import UserInDB
from models.user import User
from models.token_data import TokenData

from utils.exceptions import USERNAME_ALREADY_REGISTERED_EXCEPTION, COULD_NOT_VALIDATE_CREDENTIALS_EXCEPTION, INACTIVE_USER_EXCEPTION, INVALID_ROLE_EXCEPTION, PERMISSION_DENIED_EXCEPTION, INTERNAL_SERVER_ERROR_EXCEPTION

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = os.environ["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    user_dict = await get_user_by_username(username)
    if user_dict:
        return UserInDB(**user_dict)
    return None

async def create_account(username: str, password: str, user_data: dict):
    if await user_already_exists(username):
        raise USERNAME_ALREADY_REGISTERED_EXCEPTION
    
    hashed_password = get_password_hash(password)
    try:
        return await create_user(user_data["id_pasteleria"], username, hashed_password, user_data["deshabilitado"], user_data["email"], user_data["nombre"], user_data["apellido"])
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.clave_env):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise COULD_NOT_VALIDATE_CREDENTIALS_EXCEPTION
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise COULD_NOT_VALIDATE_CREDENTIALS_EXCEPTION
    user = await get_user(username=token_data.username)
    if user is None:
        raise COULD_NOT_VALIDATE_CREDENTIALS_EXCEPTION
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.deshabilitado:
        raise INACTIVE_USER_EXCEPTION

    return current_user

async def get_current_active_admin_user(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
):
    is_user_allowed = await is_user_admin_or_owner(current_active_user.usuario)
    if is_user_allowed is False:
        raise PERMISSION_DENIED_EXCEPTION

    return current_active_user

async def get_current_active_user_configuration(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
):
    if get_user_role_name(current_active_user.id_rol) not in role_configurations:
        raise INVALID_ROLE_EXCEPTION

    return {
        "user_config": role_configurations[get_user_role_name(current_active_user.id_rol)],
        "user_data": current_active_user
    }

def get_public_user_configuration() -> dict:
    return role_configurations["cliente"]
