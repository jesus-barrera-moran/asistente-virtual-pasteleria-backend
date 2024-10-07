from typing import Annotated, List, Optional
from fastapi import Depends, APIRouter, Form, Body
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from models.lite_user import LiteUser
from services.authentication import create_account, get_current_active_admin_user, get_current_active_user, get_password_hash, verify_password
from services.users_database import get_all_users, update_user_status, update_user_role, update_user, get_user_role_name, get_user_by_username, update_user_password

from config.roles import role_configurations

from utils.exceptions import CREDENTIALS_REQUIRED_EXCEPTION, NOT_FOUND_USER_EXCEPTION, PERMISSION_DENIED_EXCEPTION, INVALID_ROLE_EXCEPTION, INCORRECT_CREDENTIALS_EXCEPTION, INTERNAL_SERVER_ERROR_EXCEPTION

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    first_name: str = Body(...),
    last_name: str = Body(...),
    email: str = Body(...),
    username: str = Body(...),
    password: str = Body(...),
):
    if not username or not password:
        raise CREDENTIALS_REQUIRED_EXCEPTION

    user = User(
        id_pasteleria=current_user.id_pasteleria,
        username=username,
        deshabilitado=False,
        nombre=first_name,
        apellido=last_name,
        email=email,
    )

    try:
        user_data = user.dict()
        return await create_account(username, password, user_data)
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
    if current_user.usuario == username:
        raise PERMISSION_DENIED_EXCEPTION
    
    user_to_update = await get_user_by_username(username)

    if not user_to_update:
        raise NOT_FOUND_USER_EXCEPTION

    user_to_update_current_role = get_user_role_name(user_to_update["id_rol"])

    if user_to_update_current_role == "propietario":
        return PERMISSION_DENIED_EXCEPTION

    if user_to_update_current_role == "admin" and get_user_role_name(current_user.id_rol) != "propietario":
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
    if current_user.usuario == username:
        raise PERMISSION_DENIED_EXCEPTION

    if get_user_role_name(role) not in role_configurations:
        raise INVALID_ROLE_EXCEPTION

    if get_user_role_name(role) == "propietario":
        raise PERMISSION_DENIED_EXCEPTION
    
    user_to_update = await get_user_by_username(username)

    if not user_to_update:
        raise NOT_FOUND_USER_EXCEPTION

    user_to_update_current_role = get_user_role_name(user_to_update["id_rol"])

    if user_to_update_current_role == "propietario":
        return PERMISSION_DENIED_EXCEPTION

    if user_to_update_current_role == "admin" and get_user_role_name(current_user.id_rol) != "propietario":
        raise PERMISSION_DENIED_EXCEPTION

    try:
        return await update_user_role(username, role)
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.patch("/users/{username}")
async def update_user_status_and_role_endpoint(
    current_user: Annotated[User, Depends(get_current_active_admin_user)],
    username: str,
    disabled: Optional[bool] = Body(None),
    role: Optional[str] = Body(None)
):
    if current_user.usuario == username:
        raise PERMISSION_DENIED_EXCEPTION
    user_to_update = await get_user_by_username(username)
    if not user_to_update:
        raise NOT_FOUND_USER_EXCEPTION

    user_to_update_current_role = get_user_role_name(user_to_update["id_rol"])

    # Comprobar si el usuario que se está actualizando es propietario
    if user_to_update_current_role == "propietario":
        raise PERMISSION_DENIED_EXCEPTION

    # Si el usuario actual es administrador, pero no propietario, no puede cambiar roles de otros administradores
    if user_to_update_current_role == "admin" and get_user_role_name(current_user.id_rol) != "propietario":
        raise PERMISSION_DENIED_EXCEPTION

    # Si se envió un rol para actualizar
    if role:
        if get_user_role_name(role) not in role_configurations:
            raise INVALID_ROLE_EXCEPTION

        if get_user_role_name(role) == "propietario":
            raise PERMISSION_DENIED_EXCEPTION

        try:
            await update_user_role(username, role)
        except Exception as e:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

    # Si se envió un estado de deshabilitado/habilitado para actualizar
    if disabled is not None:
        try:
            await update_user_status(username, disabled)
        except Exception as e:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

    return {"message": "Usuario actualizado correctamente"}

# @router.patch("/users/batch")
# async def update_users_batch_endpoint(
#     current_user: Annotated[User, Depends(get_current_active_admin_user)],
#     users: List[LiteUser] = Body(...)
# ):
#     # Validar que el usuario actual no sea uno de los que se intenta actualizar
#     for user in users:
#         if current_user.usuario == user.username:
#             raise PERMISSION_DENIED_EXCEPTION
    
#     # Lista para recolectar usuarios que no existen
#     users_not_found = []
    
#     # Validar roles y permisos para cada usuario antes de ejecutar la actualización
#     for user in users:
#         user_to_update = await get_user_by_username(user.username)

#         if not user_to_update:
#             users_not_found.append(user.username)
#             continue

#         user_to_update_current_role = get_user_role_name(user_to_update["id_rol"])

#         # Comprobar si el usuario que se está actualizando es propietario
#         if user_to_update_current_role == "propietario":
#             raise PERMISSION_DENIED_EXCEPTION

#         # Si el usuario actual es administrador, pero no propietario, no puede cambiar roles de otros administradores
#         if user_to_update_current_role == "admin" and get_user_role_name(current_user.id_rol) != "propietario":
#             raise PERMISSION_DENIED_EXCEPTION

#         # Validar el rol enviado en la petición
#         if user.id_role:
#             if get_user_role_name(user.id_role) not in role_configurations:
#                 raise INVALID_ROLE_EXCEPTION

#             if get_user_role_name(user.id_role) == "propietario":
#                 raise PERMISSION_DENIED_EXCEPTION

#     # Si no se encontraron algunos usuarios, lanzar una excepción
#     if users_not_found:
#         raise NOT_FOUND_USER_EXCEPTION(f"Usuarios no encontrados: {', '.join(users_not_found)}")

#     try:
#         # Ejecutar la actualización batch solo después de todas las validaciones
#         updated_users = await update_users_batch([{
#             "username": user.username,
#             "disabled": user.disabled,
#             "id_role": user.id_role
#         } for user in users])
#     except Exception as e:
#         raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

#     return {"message": "Usuarios actualizados correctamente", "updated_users": updated_users}

@router.get("/users/me")
async def get_user_endpoint(
    user: Annotated[User, Depends(get_current_active_user)],
):
    return User(**user.dict())

@router.put("/users/me")
async def update_user_endpoint(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    username: str = Body(...),
    email: str = Body(...),
    first_name: str = Body(...),
    last_name: str = Body(...),
):
    if username != current_active_user.usuario:
        raise PERMISSION_DENIED_EXCEPTION

    try:
        return await update_user(
            username=current_active_user.usuario,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.put("/users/me/password")
async def update_user_password_endpoint(
    current_active_user: Annotated[User, Depends(get_current_active_user)],
    current_password: str = Body(...),
    new_password: str = Body(...),
):
    user = await get_user_by_username(current_active_user.usuario)

    if not verify_password(current_password, user['clave_env']):
        raise INCORRECT_CREDENTIALS_EXCEPTION

    try:
        return await update_user_password(
            username=current_active_user.usuario,
            new_password_hash=get_password_hash(new_password),
        )
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
