from uuid import UUID

from langchain.agents import Tool
from agents.sql_agent.agent import SQLAgent
from llms.gpt_4o.llm import llm
from tools.inventario_db.tool import inventario_db

async def agente_inventario_db(id_pasteleria: UUID):
    try:
        db = await inventario_db(id_pasteleria)
        return Tool(
            name="inventory_sql_database_agent",
            func=SQLAgent(llm=llm, db=db).get_agent().run,
            description="Useful when you need to answer questions about inventory SQL database."
        )
    except Exception as e:
        return None
