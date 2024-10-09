import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from database.engine import connect_with_connector
from typing import Optional
from uuid import UUID
from langchain_community.utilities import SQLDatabase

from utils.exceptions import INTERNAL_SERVER_ERROR_EXCEPTION

db_name = os.environ["BUSINESS_DATABASE_NAME"]

# Pasteleria and User Creation Service

async def create_pasteleria_with_admin(
    id_pasteleria: str,
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

        # 5. Crear las bases de datos de la pastelería
        session.execute(
            text(
                "INSERT INTO base_de_datos (id_pasteleria, categoria) "
                "VALUES (:id_pasteleria, 'inventario'), "
                "(:id_pasteleria, 'transacciones')"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        # 6. Crear los documentos de la pastelería
        session.execute(
            text(
                "INSERT INTO documento (id_pasteleria, nombre, bucket) "
                "VALUES (:id_pasteleria, 'catalogo', 'catalogos'), "
                "(:id_pasteleria, 'manual', 'manuales')"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        # Commit the transaction
        session.commit()

        return {
            "usuario": usuario
        }

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

async def obtener_pasteleria_por_id(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener los datos de la pastelería por su id_pasteleria
        result_pasteleria = session.execute(
            text(
                # "SELECT id, nombre, email, telefono, direccion, ciudad, codigo_postal, url_website, fecha_registro "
                "SELECT id, nombre, email, url_website "
                "FROM pasteleria "
                "WHERE id = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        pasteleria = result_pasteleria.fetchone()

        # Si no se encuentra la pastelería, devolver un mensaje informativo
        if not pasteleria:
            return {"message": "No se encontró la pastelería."}

        pasteleria_dict = {
            "id": pasteleria.id,
            "nombre": pasteleria.nombre,
            "email": pasteleria.email,
            # "telefono": pasteleria.telefono,
            # "direccion": pasteleria.direccion,
            # "ciudad": pasteleria.ciudad,
            # "codigo_postal": pasteleria.codigo_postal,
            "url_website": pasteleria.url_website,
            # "fecha_registro": pasteleria.fecha_registro
        }

        return pasteleria_dict

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

# Función para obtener todos los usuarios correspondientes a una pastelería
async def obtener_usuarios_por_pasteleria(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener todos los usuarios asociados a la pastelería por su id_pasteleria
        result_usuarios = session.execute(
            text(
                "SELECT u.id, u.usuario, u.email, r.id as rol, u.deshabilitado "
                "FROM usuario u "
                "JOIN rol r ON u.id_rol = r.id "
                "WHERE u.id_pasteleria = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        usuarios = result_usuarios.fetchall()

        # Si no se encuentran usuarios, devolver un mensaje informativo
        if not usuarios:
            return {"message": "No se encontraron usuarios para esta pastelería."}

        # Estructurar la salida en una lista de diccionarios
        lista_usuarios = [
            {
                "id_usuario": usuario.id,
                "nombre_usuario": usuario.usuario,
                "email": usuario.email,
                "rol": usuario.rol,
                "deshabilitado": usuario.deshabilitado
            }
            for usuario in usuarios
        ]

        return lista_usuarios

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

async def obtener_bases_datos_por_pasteleria(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener los datos de las bases de datos asociadas a la pastelería
        result_bases_datos = session.execute(
            text(
                "SELECT id, categoria, nombre, clave, servidor, puerto, usuario "
                "FROM base_de_datos "
                "WHERE id_pasteleria = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        bases_datos = result_bases_datos.fetchall()

        # Si no se encuentran bases de datos, devolver un mensaje informativo
        if not bases_datos:
            return {"message": "No se encontraron bases de datos para esta pastelería."}

        # Estructurar la salida en una lista de diccionarios
        lista_bases_datos = [
            {
                "id": base_dato.id,
                "categoria": base_dato.categoria,
                "nombre": base_dato.nombre,
                "clave": base_dato.clave,
                "servidor": base_dato.servidor,
                "puerto": base_dato.puerto,
                "usuario": base_dato.usuario,
            }
            for base_dato in bases_datos
        ]

        return lista_bases_datos

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

async def update_database_connection(
    id: int, nombre: str, servidor: str, puerto: int, usuario: str
):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Actualizar los datos de la conexión en la base de datos
        result = session.execute(
            text(
                """
                UPDATE base_de_datos
                SET nombre = :nombre, servidor = :servidor, puerto = :puerto, usuario = :usuario
                WHERE id = :id
                """
            ),
            {
                "nombre": nombre,
                "servidor": servidor,
                "puerto": puerto,
                "usuario": usuario,
                "id": id,
            }
        )

        session.commit()

        if result.rowcount == 0:
            raise Exception("No se encontró el registro con el ID especificado")

        return {"message": "Conexión actualizada exitosamente"}
    except Exception as exception:
        session.rollback()  # Asegurarse de hacer rollback en caso de error
        raise exception
    finally:
        session.close()

async def update_database_password(id: int, new_password: str):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Actualizar la clave en la base de datos
        result = session.execute(
            text(
                """
                UPDATE base_de_datos
                SET clave = :new_password
                WHERE id = :id
                """
            ),
            {
                "new_password": new_password,
                "id": id,
            }
        )

        session.commit()

        if result.rowcount == 0:
            raise Exception("No se encontró el registro con el ID especificado")

        return {"message": "Clave actualizada exitosamente"}
    except Exception as exception:
        session.rollback()  # Asegurarse de hacer rollback en caso de error
        raise exception
    finally:
        session.close()

async def obtener_documentos_por_pasteleria(id_pasteleria: UUID):
    engine = connect_with_connector(db_name)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Consulta para obtener los documentos asociados a la pastelería
        result_documentos = session.execute(
            text(
                "SELECT id, nombre, bucket "
                "FROM documento "
                "WHERE id_pasteleria = :id_pasteleria"
            ),
            {
                "id_pasteleria": id_pasteleria
            }
        )

        documentos = result_documentos.fetchall()

        # Si no se encuentran documentos, devolver un mensaje informativo
        if not documentos:
            return []

        # Estructurar la salida en una lista de diccionarios
        lista_documentos = [
            {
                "id": documento.id,
                "nombre": documento.nombre,
                "bucket": documento.bucket,
            }
            for documento in documentos
        ]

        return lista_documentos

    except Exception as exception:
        session.rollback()
        raise exception
    finally:
        session.close()

async def probar_conexion_base_datos(id_pasteleria: UUID, id_base_datos: int):
    # Obtener los detalles de las bases de datos asociadas a la pastelería
    bases_de_datos = await obtener_bases_datos_por_pasteleria(id_pasteleria)

    # Buscar la base de datos específica por ID
    base_de_datos_seleccionada = next(
        (base_de_datos for base_de_datos in bases_de_datos if base_de_datos["id"] == id_base_datos), None
    )

    if not base_de_datos_seleccionada:
        return {"message": f"No se encontró la base de datos con ID {id_base_datos} para la pastelería {id_pasteleria}"}

    # Extraer los detalles de conexión
    nombre = base_de_datos_seleccionada["nombre"]
    usuario = base_de_datos_seleccionada["usuario"]
    clave = base_de_datos_seleccionada["clave"]
    servidor = base_de_datos_seleccionada["servidor"]
    puerto = base_de_datos_seleccionada["puerto"]

    # Crear la cadena de conexión
    conn_str = f"postgresql+pg8000://{usuario}:{clave}@{servidor}:{puerto}/{nombre}"

    try:
        # Crear una instancia de SQLDatabase usando la cadena de conexión
        db = SQLDatabase.from_uri(conn_str)

        # Ejecutar una consulta simple para probar la conexión
        result = db.run("SELECT 1")

        # Si la consulta se ejecuta correctamente, la conexión es válida
        return {"message": "Conexión exitosa a la base de datos.", "result": result}

    except Exception as e:
        # Si ocurre un error, devolver un mensaje de error con la descripción
        raise INTERNAL_SERVER_ERROR_EXCEPTION(f"Error al conectar con la base de datos: {str(e)}")
