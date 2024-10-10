from typing import Any
from langserve.pydantic_v1 import BaseModel
from langchain.agents import AgentExecutor, create_react_agent
# from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

class Agent:
    def __init__(self, llm, tools, prompt):
        self.message_history = ChatMessageHistory()

        self.react_agent = create_react_agent(llm, tools, prompt)

        self.agent_executor = AgentExecutor(
            agent=self.react_agent,
            tools=tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True
        )

        # self.agent_with_chat_history = RunnableWithMessageHistory(
        #     self.agent_executor,
        #     # This is needed because in most real world scenarios, a session id is needed
        #     # It isn't really used here because we are using a simple in memory ChatMessageHistory
        #     lambda session_id: self.message_history,
        #     input_messages_key="input",
        #     history_messages_key="chat_history",
        # )

    def get_agent(self):
        class Input(BaseModel):
            input: str

        class Output(BaseModel):
            output: Any

        agent = self.agent_executor.with_types(input_type=Input, output_type=Output).with_config({"run_name": "agent"})
        # agent = self.agent_with_chat_history.with_types(input_type=Input, output_type=Output).with_config({"run_name": "agent"})
        return agent
