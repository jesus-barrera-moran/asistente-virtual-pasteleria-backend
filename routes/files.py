from typing import Annotated
from fastapi import Depends, APIRouter

from models.file import File
from config.general import general_configuration
from services.files_storage import read_file, write_file
from services.authentication import get_current_active_admin_user

from models.user import User

from utils.exceptions import FILE_NOT_FOUND_EXCEPTION, INTERNAL_SERVER_ERROR_EXCEPTION

router = APIRouter()

@router.post("/writeFileContent")
async def write_file_content(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    file: File
):
    try:
        if file.name not in general_configuration["file_name"]:
            raise FILE_NOT_FOUND_EXCEPTION
        write_file(
            str(current_user.id_pasteleria),
            general_configuration["file_name"][file.name],
            file.content
        )
        return {"message": f"File '{file.name}' succesfully uploaded."}
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/readFileContent")
async def read_file_content(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    file_name: str
):
    if file_name not in general_configuration["file_name"]:
        raise FILE_NOT_FOUND_EXCEPTION
    try:
        response = read_file(
            str(current_user.id_pasteleria),
            general_configuration["file_name"][file_name],
        )
        return response
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
