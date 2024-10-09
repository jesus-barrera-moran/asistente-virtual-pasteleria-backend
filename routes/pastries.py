import uuid
import secrets
import string
from typing import Annotated, List, Optional
from fastapi import Depends, APIRouter, Body, Form, UploadFile, File
from models.user import User
from services.pastries_database import create_pasteleria_with_admin, obtener_usuarios_por_pasteleria, obtener_bases_datos_por_pasteleria, update_database_connection, update_database_password, obtener_documentos_por_pasteleria, obtener_pasteleria_por_id, probar_conexion_base_datos
from services.files_storage import get_all_files_from_pasteleria, write_file, get_public_image_urls_from_pasteleria
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
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    ciudad: Optional[str] = Form(None),
    codigo_postal: Optional[int] = Form(None),
    url_website: Optional[str] = Form(None),
    logo_menu: Optional[UploadFile] = File(None),  # Campo para el archivo del logo del menú
    logo_fondo: Optional[UploadFile] = File(None),  # Campo para el archivo del logo de fondo
):
    # Generar un ID único para la pastelería
    id_pasteleria = str(uuid.uuid4())

    # Generar una contraseña segura
    raw_password = generate_secure_password()

    # Obtener el hash de la contraseña
    hashed_password = get_password_hash(raw_password)

    try:
        # Si se subió el logo del menú, guardarlo en el bucket de GCP
        if logo_menu:
            menu_logo_name = "logo_menu"
            menu_logo_content = await logo_menu.read()  # Leer el contenido del archivo
            write_file(id_pasteleria, menu_logo_name, menu_logo_content, True)  # Subir el archivo al bucket

        # Si se subió el logo de fondo, guardarlo en el bucket de GCP
        if logo_fondo:
            fondo_logo_name = "logo_fondo"
            fondo_logo_content = await logo_fondo.read()  # Leer el contenido del archivo
            write_file(id_pasteleria, fondo_logo_name, fondo_logo_content, True)  # Subir el archivo al bucket

        # Crear la pastelería y el usuario administrador en la base de datos
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

@router.get("/pastelerias/{id_pasteleria}")
async def obtener_datos_pasteleria_endpoint(
    id_pasteleria: str,
):
    try:
        # Obtener los datos de la pastelería
        pasteleria = await obtener_pasteleria_por_id(id_pasteleria)

        if "message" in pasteleria:
            raise INTERNAL_SERVER_ERROR_EXCEPTION(pasteleria["message"])

        image_urls = get_public_image_urls_from_pasteleria(id_pasteleria)

        pasteleria["logos"] = image_urls

        return pasteleria

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

@router.get("/pastelerias/{id_pasteleria}/files")
async def get_all_files(
    current_user: Annotated[User, Depends(get_current_active_admin_user)]
):
    try:
        # Verificar si el usuario tiene acceso a la pastelería actual
        folder_name = str(current_user.id_pasteleria)

        # Llamar a la función para obtener todos los archivos
        files = get_all_files_from_pasteleria(folder_name)

        if not files:
            return []

        return files

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/documentos")
async def get_all_documents(
    id_pasteleria: str,
    current_user: Annotated[User, Depends(get_current_active_admin_user)]
):
    try:
        # Verificar si el usuario tiene acceso a la pastelería actual
        if str(current_user.id_pasteleria) != id_pasteleria:
            raise PERMISSION_DENIED_EXCEPTION

        # Llamar a la función para obtener todos los documentos de la pastelería
        documentos = await obtener_documentos_por_pasteleria(uuid.UUID(id_pasteleria))

        if not documentos:
            return {"message": "No se encontraron documentos para esta pastelería."}

        return documentos

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)

@router.get("/pastelerias/{id_pasteleria}/bases-datos/{id_base_datos}/probar-conexion")
async def probar_conexion_base_datos_endpoint(
    id_pasteleria: str,
    id_base_datos: int,
    current_user: Annotated[User, Depends(get_current_active_admin_user)]
):
    try:
        # Verificar si el usuario tiene acceso a la pastelería actual
        if str(current_user.id_pasteleria) != id_pasteleria:
            raise PERMISSION_DENIED_EXCEPTION

        # Probar la conexión a la base de datos
        resultado = await probar_conexion_base_datos(uuid.UUID(id_pasteleria), id_base_datos)

        return resultado

    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
