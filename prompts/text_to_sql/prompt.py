from langchain import hub

prompt = hub.pull("rlm/text-to-sql")

prompt.template = """
Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}.

Some examples of SQL queries that corrsespond to questions are:

{few_shot_examples}

Final answer to the human will always be in Spanish.

Question: {input}
"""
