import uuid
import secrets
import string
from typing import Annotated, List, Optional
from fastapi import Depends, APIRouter, Body
from services.pastries_database import create_pasteleria_with_admin, obtener_usuarios_por_pasteleria, obtener_bases_datos_por_pasteleria, update_database_connection, update_database_password
from services.authentication import get_password_hash, get_current_active_admin_user
from utils.exceptions import INTERNAL_SERVER_ERROR_EXCEPTION, PERMISSION_DENIED_EXCEPTION

router = APIRouter()

# Función para generar una contraseña segura
def generate_secure_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

@router.post("/pastelerias")
async def create_pasteleria_endpoint(
    nombre: Annotated[str, Body()],
    email: Annotated[str, Body()],
    telefono: Annotated[Optional[str], Body()] = None,
    direccion: Annotated[Optional[str], Body()] = None,
    ciudad: Annotated[Optional[str], Body()] = None,
    codigo_postal: Annotated[Optional[int], Body()] = None,
    url_website: Annotated[Optional[str], Body()] = None,
):
    
    id_pasteleria = uuid.uuid4()

    # Generar una contraseña segura
    raw_password = generate_secure_password()

    # Obtener el hash de la contraseña
    hashed_password = get_password_hash(raw_password)

    try:
        # Crear la pastelería y el usuario administrador
        result = await create_pasteleria_with_admin(
            id_pasteleria=id_pasteleria,
            nombre=nombre,
            email=email,
            hashed_password=hashed_password,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            url_website=url_website,
        )

        return {
            "usuario": result["usuario"],
            "clave": raw_password
        }
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/usuarios")
async def obtener_usuarios_endpoint(
    id_pasteleria: str,
    current_user: Annotated[dict, Depends(get_current_active_admin_user)],
):
    try:
        # Obtener los usuarios de la pastelería
        usuarios = await obtener_usuarios_por_pasteleria(id_pasteleria)

        if str(current_user.id_pasteleria) != id_pasteleria:
            raise PERMISSION_DENIED_EXCEPTION

        if "message" in usuarios:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(usuarios["message"])

        # Formatear la respuesta para que coincida con la estructura solicitada
        users_response = [
            {
                "id": usuario["id_usuario"],
                "username": usuario["nombre_usuario"],
                "email": usuario["email"],
                "role": usuario["rol"],
                "enabled": not usuario["deshabilitado"]
            }
            for usuario in usuarios
        ]

        return users_response

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/bases-datos")
async def obtener_bases_datos_endpoint(
    id_pasteleria: str,
    current_user: Annotated[dict, Depends(get_current_active_admin_user)],
):
    try:
        # Verificar si el usuario tiene permiso para acceder a la información de la pastelería
        if str(current_user.id_pasteleria) != id_pasteleria:
            raise PERMISSION_DENIED_EXCEPTION

        # Obtener las bases de datos asociadas a la pastelería
        bases_datos = await obtener_bases_datos_por_pasteleria(uuid.UUID(id_pasteleria))

        if "message" in bases_datos:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(bases_datos["message"])

        return bases_datos

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.put("/bases-datos/{id}")
async def actualizar_datos_conexion(
    id: int,
    nombre: Annotated[str, Body()],
    servidor: Annotated[str, Body()],
    puerto: Annotated[int, Body()],
    usuario: Annotated[str, Body()],
    _: Annotated[dict, Depends(get_current_active_admin_user)]
):
    try:
        # Actualizar los datos de la conexión
        result = await update_database_connection(
            id=id,
            nombre=nombre,
            servidor=servidor,
            puerto=puerto,
            usuario=usuario
        )

        return result

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.put("/bases-datos/{id}/clave")
async def actualizar_clave_conexion(
    id: int,
    new_password: Annotated[str, Body()],
    _: Annotated[dict, Depends(get_current_active_admin_user)]
):
    try:

        # Actualizar la clave de la conexión
        result = await update_database_password(
            id=id,
            new_password=new_password
        )

        return result

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
