import docx
import pdfplumber


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
