from langchain.agents import Tool
from agents.sql_agent.agent import SQLAgent
from llms.gpt_4o.llm import llm
from tools.transacciones_db.tool import db

tool = Tool(
    name="transactions_sql_database_agent",
    func=SQLAgent(llm=llm, db=db).get_agent().run,
    description="Useful when you need to answer questions about transactions SQL database."
)
