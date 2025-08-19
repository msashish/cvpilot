from config import ANTHROPIC_API_KEY, GEMINI_API_KEY
from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader, TextLoader

# Alternative for embeddings if you don't have OpenAI API
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic


class DocumentQASystem:
    def __init__(self, anthropic_api_key, document_path):
        """Initialize the QA system with Claude and a document"""
        self.anthropic_api_key = anthropic_api_key
        self.document_path = document_path
        self.vectorstore = None
        self.qa_chain = None
        
        # Initialize Claude
        self.llm = ChatAnthropic(
            api_key=anthropic_api_key,
            model="claude-3-sonnet-20240229",
            temperature=0.1,
            max_tokens=1000
        )
        
    def load_and_split_document(self):
        """Load document and split into chunks"""
        # Choose loader based on file type
        if self.document_path.endswith('.pdf'):
            loader = PyPDFLoader(self.document_path)
        else:
            loader = TextLoader(self.document_path, encoding='utf-8')
        
        # Load the document
        documents = loader.load()
        
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Split document into {len(chunks)} chunks")
        return chunks
    
    def create_vectorstore(self, chunks):
        """Create vector store from document chunks"""
        # Use HuggingFace embeddings (free) instead of OpenAI
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        print("Vector store created successfully")
        return self.vectorstore
    
    def create_qa_chain(self):
        """Create the QA chain"""
        if not self.vectorstore:
            raise ValueError("Vector store not created. Run create_vectorstore first.")
        
        # Create custom prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.

        Context: {context}

        Question: {question}
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}  # Retrieve top 3 relevant chunks
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
        print("QA chain created successfully")
        return self.qa_chain
    
    def ask_question(self, question):
        """Ask a question about the document"""
        if not self.qa_chain:
            raise ValueError("QA chain not created. Run create_qa_chain first.")
        
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "source_documents": result["source_documents"]
        }
    
    def setup_complete_system(self):
        """Setup the complete QA system"""
        print("Loading and splitting document...")
        chunks = self.load_and_split_document()
        
        print("Creating vector store...")
        self.create_vectorstore(chunks)
        
        print("Creating QA chain...")
        self.create_qa_chain()
        
        print("QA system ready!")

# Example usage
def main():
    # Set your API key
    ANTHROPIC_API_KEY = "your-anthropic-api-key-here"  # Or use environment variable
    DOCUMENT_PATH = "your_document.txt"  # Path to your document
    
    # Create QA system
    qa_system = DocumentQASystem(ANTHROPIC_API_KEY, DOCUMENT_PATH)
    
    # Setup the complete system
    qa_system.setup_complete_system()
    
    # Ask questions
    questions = [
        "What is the main topic of this document?",
        "Can you summarize the key points?",
        "What are the conclusions mentioned?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        result = qa_system.ask_question(question)
        print(f"Answer: {result['answer']}")
        print(f"Sources used: {len(result['source_documents'])} chunks")
        print("-" * 50)

if __name__ == "__main__":
    main()

# Alternative: Simple function-based approach
# def simple_qa_setup(api_key, document_path, question):
#     """Simplified version for quick setup"""
#     # Load document
#     if document_path.endswith('.pdf'):
#         loader = PyPDFLoader(document_path)
#     else:
#         loader = TextLoader(document_path)

#     documents = loader.load()

#     # Split text
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(documents)

#     # Create embeddings and vector store
#     embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     vectorstore = Chroma.from_documents(chunks, embeddings)

#     # Create LLM
#     llm = ChatAnthropic(api_key=api_key, model="claude-3-sonnet-20240229")

#     # Create QA chain
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever()
#     )

#     # Ask question
#     result = qa_chain({"query": question})
#     return result["result"]

# Usage example:
# answer = simple_qa_setup("your-api-key", "document.txt", "What is this document about?")
# print(answer)

def build_qa_chain(documents):

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Create embeddings and vector store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings)

    # Create LLM
    llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY, model="claude-3-sonnet-20240229")

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    return qa_chain
