import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from database.engine import connect_with_connector
from typing import Optional
from uuid import UUID

db_name = os.environ["BUSINESS_DATABASE_NAME"]

# Pasteleria and User Creation Service

async def create_pasteleria_with_admin(
    id_pasteleria: UUID,
    nombre: str, 
    email: str, 
    hashed_password: str,
    telefono: Optional[str] = None, 
    direccion: Optional[str] = None, 
    ciudad: Optional[str] = None, 
    codigo_postal: Optional[str] = None, 
    url_website: Optional[str] = None, 
):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 1. Crear registro de pastelería
        result_pasteleria = session.execute(
            text(
                "INSERT INTO pasteleria (id, nombre, email, telefono, direccion, ciudad, codigo_postal, url_website, fecha_registro)"
                "VALUES (:id, :nombre, :email, :telefono, :direccion, :ciudad, :codigo_postal, :url_website, NOW()) "
                "RETURNING id"
            ),
            {
                "id": id_pasteleria,
                "nombre": nombre, 
                "email": email, 
                "telefono": telefono, 
                "direccion": direccion, 
                "ciudad": ciudad, 
                "codigo_postal": codigo_postal, 
                "url_website": url_website
            }
        )
        id_pasteleria = result_pasteleria.fetchone()[0]

        # 2. Obtener el ID del rol "propietario"
        result_role = session.execute(
            text("SELECT id FROM rol WHERE nombre = 'propietario'")
        )

        role_row = result_role.fetchone()
        
        if role_row is None:
            raise Exception("Role not found")

        id_role = role_row[0]

        usuario = "propietario_" + nombre.lower().replace(" ", "_")

        # 4. Crear el usuario con las credenciales de la pastelería
        session.execute(
            text(
                "INSERT INTO usuario (id_pasteleria, id_rol, usuario, clave_env, deshabilitado) "
                "VALUES (:id_pasteleria, :id_role, :username, :hashed_password, false)"
            ),
            {
                "id_pasteleria": id_pasteleria,
                "id_role": id_role,
                "username": usuario,
                "hashed_password": hashed_password,
            }
        )

        # Commit the transaction
        session.commit()

        return {
            "pasteleria": {
                "id": id_pasteleria,
                "nombre": nombre,
                "email": email
            },
            "propietario": {
                "usuario": usuario,
                "rol": "propietario",
                "clave_env": 1234
            }
        }

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()
