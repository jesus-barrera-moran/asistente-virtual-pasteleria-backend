from fastapi import HTTPException, status

COULD_NOT_VALIDATE_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"}
)

USERNAME_ALREADY_REGISTERED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="El nombre de usuario ya está registrado"
)

INACTIVE_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Usuario inactivo"
)

INVALID_ROLE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Rol no válido"
)

FILE_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Archivo no encontrado en la configuración general"
)

PERMISSION_DENIED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No tienes permiso para realizar esta acción"
)

CREDENTIALS_REQUIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="El nombre de usuario y la contraseña son obligatorios"
)

INCORRECT_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Nombre de usuario o contraseña incorrectos",
    headers={"WWW-Authenticate": "Bearer"}
)

NOT_ALLOWED_ACTION_EXCEPTION = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Acción no permitida"
)

NOT_FOUND_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Usuario no encontrado"
)

def INTERNAL_SERVER_ERROR_EXCEPTION(e: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )
