import asyncio
from uuid import UUID
from langchain_community.utilities import SQLDatabase
from services.pastries_database import obtener_bases_datos_por_pasteleria
from utils.exceptions import INTERNAL_SERVER_ERROR_EXCEPTION

async def transacciones_db(id_pasteleria: UUID):
    categoria = "transacciones"

    # Obtener bases de datos disponibles para la pastelería
    bases_de_datos = await obtener_bases_datos_por_pasteleria(id_pasteleria)

    # Filtrar la base de datos de transacciones
    bases_de_datos_transacciones = [base_de_datos for base_de_datos in bases_de_datos if base_de_datos["categoria"] == categoria]

    if not bases_de_datos_transacciones:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(f"Database {categoria} not found for bakery {id_pasteleria}")

    name = bases_de_datos_transacciones[0]["nombre"]
    user = bases_de_datos_transacciones[0]["usuario"]
    password = bases_de_datos_transacciones[0]["clave"]
    host = bases_de_datos_transacciones[0]["servidor"]
    puerto = bases_de_datos_transacciones[0]["puerto"]

    # Crear la cadena de conexión
    conn_str = f"postgresql+pg8000://{user}:{password}@{host}:{puerto}/{name}"

    # Intentar la conexión con un timeout de 5 segundos usando asyncio.wait_for
    try:
        db = await asyncio.wait_for(
            asyncio.to_thread(SQLDatabase.from_uri, conn_str),  # Ejecutar en un hilo separado
            timeout=5  # Timeout de 5 segundos
        )
        return db

    except asyncio.TimeoutError:
        # Manejar el caso de timeout
        print(f"Timeout al intentar conectar a la base de datos de transacciones para la pastelería {id_pasteleria}")
        raise INTERNAL_SERVER_ERROR_EXCEPTION(f"Connection timeout for bakery {id_pasteleria}")
