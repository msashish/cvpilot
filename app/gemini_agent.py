import google.generativeai as genai
from chromadb.config import Settings
from config import GEMINI_API_KEY
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
#from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY, transport='rest')
#model = genai.GenerativeModel("gemini-1.5-pro")
model = genai.GenerativeModel("gemini-2.0-flash")

def evaluate_cv(cv_text, jd_text):  # noqa: ANN001, ANN201, D103

    # Prompt template
    prompt = f"""
    You are a hiring assistant AI.

    Evaluate the following resume against the given job description for a 'Senior GCP Engineer' role.

    ---
    Job Description:
    {jd_text}
    ---
    Resume:
    {cv_text}
    ---

    Please provide:
    1. A summary of how well the resume matches the job requirements.
    2. Key strengths of the candidate based on the resume.
    3. Gaps or missing skills if any.
    4. Final recommendation: "Strong Fit", "Moderate Fit", or "Not a Fit", with reasoning.
    """
    # Generate response
    response = model.generate_content(prompt)
    return response.text


# def build_qa_chain(documents):

#     # Split text
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(documents)

#     # Create embeddings and vector store
#     #embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#     embeddings = HuggingFaceEmbeddings(
#                 model_name="all-MiniLM-L6-v2",
#                 model_kwargs={"device": "cpu"}  # force normal load on CPU
#                 )
#     print("Embeddings successfully created")
#     vectorstore = Chroma.from_documents(
#         chunks, 
#         embeddings,
#         persist_directory=""
#         )
#     print("Embeddings successfully stored in Chroma DB")

#      # 4️⃣ Create Gemini LLM
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",  # free-tier model
#         google_api_key=GEMINI_API_KEY,
#         temperature=0.2
#     )

#     # 5️⃣ Create RetrievalQA chain
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever()
#     )

#     return qa_chain
