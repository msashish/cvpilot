from chromadb.config import Settings
from config import ANTHROPIC_API_KEY
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic


def build_qa_chain(documents):

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Create embeddings and vector store
    #embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}  # force normal load on CPU
                )
    print("Embeddings successfully created")
    vectorstore = Chroma.from_documents(
        chunks, 
        embeddings,
        persist_directory=""
        )
    print("Embeddings successfully stored in Chroma DB")

    # Create LLM
    #llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model="claude-3-5-sonnet-20240620")
    #llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model="claude-3-haiku-20240307")
    #llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model="claude-opus-4-20250514")
    llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model="claude-3-5-sonnet-20240229")

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    return qa_chain
