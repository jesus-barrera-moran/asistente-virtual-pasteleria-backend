import uuid
from typing import Annotated, Optional
from fastapi import Depends, APIRouter, Body
from services.pastries_database import create_pasteleria_with_admin
from services.authentication import get_password_hash
from utils.exceptions import INTERNAL_SERVER_ERROR_EXCEPTION

router = APIRouter()

@router.post("/pastelerias")
async def create_pasteleria_endpoint(
    nombre: Annotated[str, Body()],
    email: Annotated[str, Body()],
    telefono: Annotated[Optional[str], Body()] = None,
    direccion: Annotated[Optional[str], Body()] = None,
    ciudad: Annotated[Optional[str], Body()] = None,
    codigo_postal: Annotated[Optional[str], Body()] = None,
    url_website: Annotated[Optional[str], Body()] = None,
):
    
    id_pasteleria = uuid.uuid4()

    # Obtener el hash de la contraseña
    hashed_password = get_password_hash('1234')

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
            "message": "Pastelería y usuario administrador creados con éxito",
            "pasteleria": result["pasteleria"],
            "propietario": result["propietario"]
        }
    except Exception as e:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(e)
