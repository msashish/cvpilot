import tempfile

import docx
import pdfplumber
from langchain.document_loaders import PyPDFLoader, WebBaseLoader


def extract_text_from_file(path):
    if path.endswith(".txt"):
        with open(path) as f:
            return f.read()
    elif path.endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif path.endswith(".docx"):
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise ValueError("Unsupported file type")


def load_pdf(file_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_path.read())
        tmp_path = tmp_file.name
    loader = PyPDFLoader(tmp_path)
    return loader.load()

def load_webpage(url):
    loader = WebBaseLoader(url)
    return loader.load()
