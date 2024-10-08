from uuid import UUID

# from langchain.agents import Tool
# from langchain_experimental.sql import SQLDatabaseChain
# from llms.gpt_4o.llm import llm
# import os

from langchain_community.utilities import SQLDatabase

from services.pastries_database import obtener_bases_datos_por_pasteleria

from utils.exceptions import INTERNAL_SERVER_ERROR_EXCEPTION

async def transacciones_db(id_pasteleria: UUID):
    # Get the database name, user and password from environment variables
    categoria = "transacciones"

    bases_de_datos = await obtener_bases_datos_por_pasteleria(id_pasteleria)

    bases_de_datos_inventario = [base_de_datos for base_de_datos in bases_de_datos if base_de_datos["categoria"] == categoria]

    if not bases_de_datos_inventario:
        raise INTERNAL_SERVER_ERROR_EXCEPTION(f"Database {categoria} not found for bakery {id_pasteleria}")
    
    name = bases_de_datos_inventario[0]["nombre"]
    user = bases_de_datos_inventario[0]["usuario"]
    password = bases_de_datos_inventario[0]["clave"]
    host = bases_de_datos_inventario[0]["servidor"]
    puerto = bases_de_datos_inventario[0]["puerto"]

    # Create the connection string
    conn_str = f"postgresql+pg8000://{user}:{password}@{host}:{puerto}/{name}"

    # Create the SQLDatabase instance using the connection string
    db = SQLDatabase.from_uri(conn_str)

    return db

    # Crear la cadena SQLDatabaseChain usando la base de datos en la nube
    # sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    # # Crear la herramienta usando la cadena SQLDatabaseChain
    # return Tool(
    #     name="transactions_db",
    #     func=sql_chain.run,
    #     description="Useful when you need to answer questions about transactions' database."
    # )
