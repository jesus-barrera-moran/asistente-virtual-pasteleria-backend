from llms.gpt_4o.llm import llm as gpt_4o_llm

from tools.catalogo_doc.tool import tool as catalogo_doc
from tools.manual_doc.tool import tool as manual_doc
from tools.agente_inventario_db.tool import agente_inventario_db
from tools.agente_transacciones_db.tool import agente_transacciones_db

from prompts.react_chat.prompt import prompt as customer_support_prompt

# Función asíncrona para obtener las herramientas de cada rol
async def obtener_herramientas_propietario(id_pasteleria):
    return [
        await catalogo_doc(id_pasteleria),
        await manual_doc(id_pasteleria),
        await agente_inventario_db(id_pasteleria),
        await agente_transacciones_db(id_pasteleria),
    ]

async def obtener_herramientas_admin(id_pasteleria):
    return [
        await catalogo_doc(id_pasteleria),
        await manual_doc(id_pasteleria),
        await agente_inventario_db(id_pasteleria),
        await agente_transacciones_db(id_pasteleria),
    ]

async def obtener_herramientas_empleado(id_pasteleria):
    return [
        await catalogo_doc(id_pasteleria),
        await manual_doc(id_pasteleria),
    ]

async def obtener_herramientas_cliente(id_pasteleria):
    return [
        await catalogo_doc(id_pasteleria),
    ]

# Define roles configuration utilizando las funciones asíncronas
role_configurations = {
    "propietario": {
        "tools": obtener_herramientas_propietario,
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
    "admin": {
        "tools": obtener_herramientas_admin,
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
    "empleado": {
        "tools": obtener_herramientas_empleado,
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
    "cliente": {
        "tools": obtener_herramientas_cliente,
        "prompt": customer_support_prompt,
        "llm": gpt_4o_llm,
    },
}
