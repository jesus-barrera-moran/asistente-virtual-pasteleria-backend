import os

from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from services.files_storage import read_file
from config.general import general_configuration

def tool():
    os.makedirs('documents', exist_ok=True)
    file_data = read_file(
        general_configuration["bucket_name"],
        general_configuration["file_name"]["manual"]
    )

    file_content = file_data["content"].decode('utf-8')
    file_path = os.path.join('documents', file_data["name"])

    with open(file_path, "w") as file:
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
        "Useful when you need to anser questions about to do pastry's processes.",
    )

    return tool
