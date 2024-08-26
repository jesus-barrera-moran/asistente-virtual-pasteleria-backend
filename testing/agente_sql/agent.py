from typing import Any

from langserve.pydantic_v1 import BaseModel

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from llms.gpt_3_turbo.llm import llm

message_history = ChatMessageHistory()

db = SQLDatabase.from_uri("sqlite:///catalogo_2.db")

agent_executor = create_sql_agent(
    llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
    max_iterations=5,
    # handle_parsing_errors=True
)

# agent_with_chat_history = RunnableWithMessageHistory(
#     agent_executor,
#     # This is needed because in most real world scenarios, a session id is needed
#     # It isn't really used here because we are using a simple in memory ChatMessageHistory
#     lambda session_id: message_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
# )

class Input(BaseModel):
    input: str

class Output(BaseModel):
    output: Any

# agent = agent_with_chat_history.with_types(input_type=Input, output_type=Output).with_config({"run_name": "agent"})
agent = agent_executor.with_types(input_type=Input, output_type=Output).with_config({"run_name": "agent"})
