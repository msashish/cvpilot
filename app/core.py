from config import CHAT_OPENAI_API_KEY
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

# This code is a classic RAG (Retrieval-Augmented Generation) pipeline:
    # Documents → Split → Embed → Store → Retrieve → Answer with LLM

# Does following:
    # Takes in a set of documents (docs)
    # Splits them into smaller chunks
    # Embeds them into a vector store (FAISS). FAISS is a vector search engine.
        # It stores embeddings and can efficiently search for nearest neighbors (similar chunks) given a query vector.
    # Creates a retriever to find the most relevant chunks for a query
    # Wraps it all into a RetrievalQA chain so you can ask natural language questions against the documents.

# LangChain is designed around modularity and composability:
    # Document Loaders → bring in your data
    # Text Splitters → chunk your data for efficient processing
    # Embeddings Models → convert text into vectors
    # Vector Stores → store and search embeddings
    # Retrievers → abstract retrieval from storage
    # Chains → link together LLMs + tools + retrievers into workflows
    # Agents (optional) → dynamically choose tools/chains at runtime

def build_qa_chain(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=CHAT_OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(temperature=0, openai_api_key=CHAT_OPENAI_API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return qa_chain
