from langchain.agents import Tool
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from llms.gpt_4o.llm import llm
import os

name=os.environ["TRANSACTIONS_DATABASE_NAME"]
instance_connection_name = os.environ["DATABASE_INSTANCE_CONNECTION_NAME"]
user = os.environ["DATABASE_INSTANCE_USER"]
password = os.environ["DATABASE_INSTANCE_PASSWORD"]

# Create the connection string
conn_str = f"postgresql+pg8000://{user}:{password}@localhost:5432/{name}"

# Create the SQLDatabase instance using the connection string
db = SQLDatabase.from_uri(conn_str)

# Crear la cadena SQLDatabaseChain usando la base de datos en la nube
sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Crear la herramienta usando la cadena SQLDatabaseChain
tool = Tool(
    name="transactions_db",
    func=sql_chain.run,
    description="Useful when you need to answer questions about transactions' database."
)
