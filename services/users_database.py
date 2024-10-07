import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from database.engine import connect_with_connector
from typing import Optional
from uuid import UUID

from utils.exceptions import NOT_FOUND_USER_EXCEPTION

db_name = os.environ["BUSINESS_DATABASE_NAME"]

async def get_all_users():
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text("SELECT * FROM usuario"))
        rows = result.fetchall()

        users = []
        for row in rows:
            row_dict = {column: value for column, value in zip(result.keys(), row)}
            users.append(row_dict)

        return users
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def get_user_by_username(username: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("SELECT * FROM usuario WHERE usuario = :username"),
            {"username": username}
        )

        row = result.fetchone()

        if row is None:
            raise NOT_FOUND_USER_EXCEPTION

        return {column: value for column, value in zip(result.keys(), row)}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_user_status(username: str, disabled: bool):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("UPDATE usuario SET deshabilitado = :disabled WHERE usuario = :username"),
            {"username": username, "disabled": disabled}
        )

        session.commit()

        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"username": username, "disabled": disabled}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_user_role(username: str, id_role: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result_role = session.execute(
            text("SELECT id FROM rol WHERE id = :id_role"),
            {"id_role": id_role}
        )
        role_row = result_role.fetchone()

        if role_row is None:
            raise Exception("Role not found")

        id_role = role_row[0]

        result = session.execute(
            text("UPDATE usuario SET id_rol = :id_role WHERE usuario = :username"),
            {"username": username, "id_role": id_role}
        )

        session.commit()

        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"username": username, "id_role": id_role}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_users_batch(users: list[dict]):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Recolectar todos los usernames y roles
        roles = [user["id_role"] for user in users]

        # Validar que todos los roles existen
        result_roles = session.execute(
            text("SELECT id FROM rol WHERE id IN :roles"),
            {"roles": tuple(roles)}
        )
        found_roles = [row[0] for row in result_roles.fetchall()]

        # Verificar si hay roles inexistentes
        missing_roles = set(roles) - set(found_roles)
        if missing_roles:
            raise Exception(f"Roles no encontrados: {', '.join(missing_roles)}")
        # Preparar el SQL batch para actualizar todos los usuarios
        update_queries = []
        for user in users:
            update_queries.append(
                f"UPDATE usuario SET deshabilitado = :disabled_{user['username']}, id_rol = :id_role_{user['username']} WHERE usuario = :username_{user['username']}"
            )
        # Crear la consulta combinada
        combined_update_query = "; ".join(update_queries)
        
        # Parámetros para la consulta
        parameters = {}
        for user in users:
            parameters.update({
                f"username_{user['username']}": user["username"],
                f"disabled_{user['username']}": user["disabled"],
                f"id_role_{user['username']}": user["id_role"],
            })
        # Ejecutar la consulta de actualización en batch
        result = session.execute(
            text(combined_update_query),
            parameters
        )
        session.commit()

        return [{"username": user["username"], "disabled": user["disabled"], "id_role": user["id_role"]} for user in users]

    except Exception as exception:
        session.rollback()  # Hacer rollback si ocurre algún error
        raise exception
    finally:
        session.close()

async def update_user(username: str, email: str, first_name: str, last_name: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        update_data = {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }

        result = session.execute(
            text(
                "UPDATE usuario SET email = :email, nombre = :first_name, apellido = :last_name WHERE usuario = :username"
            ),
            update_data
        )

        session.commit()

        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"username": username, "email": email, "first_name": first_name, "last_name": last_name}
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def user_already_exists(username: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(
            text("SELECT * FROM usuario WHERE usuario = :username"),
            {"username": username}
        )

        return result.fetchone() is not None
    except Exception as exception:
        raise exception
    finally:
        session.close()

async def update_user_password(username: str, new_password_hash: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Actualizar la contraseña en la base de datos
        result = session.execute(
            text("UPDATE usuario SET clave_env = :new_password WHERE usuario = :username"),
            {"new_password": new_password_hash, "username": username}
        )

        session.commit()

        # Verificar si se actualizó correctamente
        if result.rowcount == 0:
            raise NOT_FOUND_USER_EXCEPTION

        return {"message": "Contraseña actualizada exitosamente"}
    except Exception as exception:
        session.rollback()  # Asegurarse de hacer rollback en caso de error
        raise exception
    finally:
        session.close()

async def create_user(id_pasteleria: UUID, username: str, hashed_password: str, deshabilitado: bool, email: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Obtener el ID del rol "empleado"
        result_role = session.execute(
            text("SELECT id FROM rol WHERE nombre = 'empleado'")
        )
        role_row = result_role.fetchone()

        if role_row is None:
            raise Exception("Role not found")

        # role_row es una tupla, por lo que extraemos el valor del ID del rol
        id_role = role_row[0]

        # Insertar el usuario en la base de datos
        session.execute(
            text(
                "INSERT INTO usuario (id_pasteleria, id_rol, usuario, clave_env, deshabilitado, email, nombre, apellido) "
                "VALUES (:id_pasteleria, :id_role, :username, :hashed_password, :disabled, :email, :first_name, :last_name)"
            ),
            {
                "id_pasteleria": id_pasteleria,
                "id_role": id_role,
                "username": username,
                "hashed_password": hashed_password,
                "disabled": deshabilitado,
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
        )

        # Confirmar la transacción
        session.commit()

        # Retornar los datos del usuario creado
        return {
            "id_pasteleria": id_pasteleria,
            "id_rol": id_role,
            "usuario": username,
            "deshabilitado": deshabilitado,
            "email": email,
            "nombre": first_name,
            "apellido": last_name
        }

    except Exception as exception:
        # En caso de error, hacer rollback
        session.rollback()
        raise exception
    finally:
        # Cerrar la sesión
        session.close()

async def is_user_admin_or_owner(username: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener el rol del usuario
        result = session.execute(
            text(
                "SELECT r.nombre FROM usuario u "
                "JOIN rol r ON u.id_rol = r.id "
                "WHERE u.usuario = :username"
            ),
            {"username": username}
        )

        row = result.fetchone()

        if row is None:
            raise NOT_FOUND_USER_EXCEPTION("Usuario no encontrado")

        role_name = row[0]
        # Verificar si el rol es administrador o propietario
        if role_name.lower() in ["admin", "propietario"]:
            return True

        return False

    except Exception as e:
        raise e
    finally:
        session.close()

# Mock temporary implementation
def get_user_role_name(id_rol: str):
    rol_number = int(id_rol)
    if rol_number == 11:
        return "admin"
    elif rol_number == 12:
        return "empleado"
    elif rol_number == 13:
        return "cliente"
    elif rol_number == 17:
        return "propietario"
    else:
        return "unknown"
