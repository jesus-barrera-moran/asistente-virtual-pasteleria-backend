from typing import Annotated, Optional
from fastapi import Depends, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from services.authentication import create_account, get_current_active_admin_user, get_current_active_user, get_password_hash
from services.users_database import get_all_users, update_user_status, update_user_role, update_user

from config.roles import role_configurations

from utils.exceptions import CREDENTIALS_REQUIRED_EXCEPTION, PERMISSION_DENIED_EXCEPTION, INVALID_ROLE_EXCEPTION, INTERNAL_SERVER_ERROR_EXCEPTION

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(
    _: Annotated[User, Depends(get_current_active_admin_user)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    if not form_data.username or not form_data.password:
        raise CREDENTIALS_REQUIRED_EXCEPTION

    user = User(
        username=form_data.username,
        role="employee",
        disabled=False
    )

    try:
        user_data = user.dict()
        return await create_account(form_data.username, form_data.password, user_data)
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/users")
async def get_users_endpoint(
    _: Annotated[User, Depends(get_current_active_admin_user)]
):
    users = []
    try:
        users_in_db = await get_all_users()
        users = [User(**user) for user in users_in_db]
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

    return users

@router.patch("/users/{username}/status")
async def update_user_status_endpoint(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    username: str,
    disabled: bool = Form(...)
):
    if current_user.username == username:
        raise PERMISSION_DENIED_EXCEPTION

    try:
        return await update_user_status(username, disabled)
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.patch("/users/{username}/role")
async def update_user_role_endpoint(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    username: str,
    role: str = Form(...)
):
    if current_user.username == username:
        raise PERMISSION_DENIED_EXCEPTION

    if role not in role_configurations:
        raise INVALID_ROLE_EXCEPTION

    try:
        return await update_user_role(username, role)
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/users/me")
async def get_user_endpoint(
    user: Annotated[User, Depends(get_current_active_user)],
):
    return User(**user.dict())

@router.put("/users/me")
async def update_user_endpoint(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    email: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
):
    if form_data.username != current_active_user.username:
        raise PERMISSION_DENIED_EXCEPTION

    if not form_data.username or not form_data.password:
        raise CREDENTIALS_REQUIRED_EXCEPTION

    try:
        return await update_user(
            username=current_active_user.username,
            new_hashed_password=get_password_hash(form_data.password),
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
