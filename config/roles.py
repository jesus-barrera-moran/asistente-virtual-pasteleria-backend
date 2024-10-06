from llms.gpt_4o.llm import llm as gpt_4o_llm

from tools.catalogo_doc.tool import tool as catalogo_doc
from tools.manual_doc.tool import tool as manual_doc
# from tools.agente_inventario_db.tool import tool as agente_inventario_db
# from tools.agente_transacciones_db.tool import tool as agente_transacciones_db

# from prompts.text_to_sql.prompt import prompt as text_to_sql_prompt
# from prompts.admin.prompt import prompt as admin_prompt
from prompts.react_chat.prompt import prompt as customer_support_prompt

role_configurations = {
    "propietario": {
        # "tools": lambda: [catalogo_doc(), manual_doc(), agente_inventario_db, agente_transacciones_db],
        "tools": lambda id_pasteleria: [catalogo_doc(id_pasteleria), manual_doc(id_pasteleria)],
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
    "admin": {
        # "tools": lambda: [catalogo_doc(), manual_doc(), agente_inventario_db, agente_transacciones_db],
        "tools": lambda id_pasteleria: [catalogo_doc(id_pasteleria), manual_doc(id_pasteleria)],
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
    "empleado": {
        "tools": lambda id_pasteleria: [catalogo_doc(id_pasteleria), manual_doc(id_pasteleria)],
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
    "cliente": {
        "tools": lambda id_pasteleria: [catalogo_doc(id_pasteleria)],
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
}
