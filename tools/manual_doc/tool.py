import os

from uuid import UUID
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from services.files_storage import read_file
from config.general import general_configuration

async def tool(id_pasteleria: UUID):
    id_pasteleria_str = str(id_pasteleria)
    folder_name = f"documents/{id_pasteleria_str}"
    os.makedirs(folder_name, exist_ok=True)
    file_data = read_file(
        id_pasteleria_str,
        general_configuration["file_name"]["manual"]
    )

    file_content = "No existen procesos disponibles en el manual."

    # Verificar si el contenido del archivo está vacío
    if file_data["content"]:
        file_content = file_data["content"].decode('utf-8')

    file_path = os.path.join(folder_name, file_data["name"])

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_content)

    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)

    retriever = db.as_retriever()

    tool = create_retriever_tool(
        retriever,
        "manual_doc",
        "Useful when you need to answer questions about to do pastry's processes.",
    )

    return tool
