from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from models.token import Token
from services.authentication import create_access_token, authenticate_user

from utils.exceptions import INCORRECT_CREDENTIALS_EXCEPTION

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise INCORRECT_CREDENTIALS_EXCEPTION

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
