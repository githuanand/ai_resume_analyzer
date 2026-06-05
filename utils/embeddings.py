from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def create_vectorstore(text):

    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(
        chunks,
        embeddings
    )

    return vectorstore