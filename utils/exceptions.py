from fastapi import HTTPException, status

COULD_NOT_VALIDATE_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

USERNAME_ALREADY_REGISTERED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already registered"
)

INACTIVE_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user"
)

INVALID_ROLE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid role"
)

FILE_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="File not found in general configuration"
)

PERMISSION_DENIED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to perform this action"
)

CREDENTIALS_REQUIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username and password are required"
)

INCORRECT_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)

NOT_ALLOWED_ACTION_EXCEPTION = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail="Not allowed action"
)

NOT_FOUND_USER_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

def INTERNAL_SERVER_ERROR_EXCEPTION(e: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(e)
    )
