from uuid import UUID

from langchain.agents import Tool
from agents.sql_agent.agent import SQLAgent
from llms.gpt_4o.llm import llm
from tools.transacciones_db.tool import tool

async def tool(id_pasteleria: UUID):
    db_tool = tool(id_pasteleria)
    return Tool(
        name="transactions_sql_database_agent",
        func=SQLAgent(llm=llm, db=db_tool).get_agent().run,
        description="Useful when you need to answer questions about transactions SQL database."
    )
