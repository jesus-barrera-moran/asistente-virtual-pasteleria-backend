from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class User(BaseModel):
    id: Optional[int] = None
    id_pasteleria: Optional[UUID] = None
    id_rol: Optional[int] = None
    usuario: Optional[str] = None
    email: Optional[str] = None
    clave_env: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    deshabilitado: Optional[bool] = None
