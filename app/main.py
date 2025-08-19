import streamlit as st
from claude_agent import build_qa_chain
from gemini_agent import evaluate_cv
from utils import load_pdf, load_webpage

st.set_page_config(layout="wide")

st.title("📄🔍 CV Assistant AI")

# Initialize session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "user_questions" not in st.session_state:
    st.session_state.user_questions = ""

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("CV Input")
    cv_source = st.radio("Choose your CV format", ["PDF", "Web Page"], key="cv_source")
    cv_content = []
    if cv_source == "PDF":
        uploaded_file = st.file_uploader("Upload a PDF", type="pdf", key="cv_uploader")
        if uploaded_file:
            cv_content = load_pdf(uploaded_file)
    elif cv_source == "Web Page":
        url = st.text_input("Enter a URL", key="cv_url")
        if url:
            cv_content = load_webpage(url)


with col2:
    st.subheader("Job Description Input")
    jd_source = st.radio("Choose your JD format", ["PDF", "Text", "Web Page"], key="jd_source")
    jd_content = []
    if jd_source == "PDF":
        uploaded_file = st.file_uploader("Upload a PDF", type="pdf", key="jd_uploader")
        if uploaded_file:
            jd_content = load_pdf(uploaded_file)
    elif jd_source == "Web Page":
        url = st.text_input("Enter a URL", key="jd_url")
        if url:
            jd_content = load_webpage(url)
    elif jd_source == "Text":
        jd_content = [st.text_area("Enter JD text", key="user_input")]

# Process on button click
if st.button("Evaluate Fitment"):
    if not cv_content or not jd_content:
        st.error("Please upload a CV and enter a Job Description first")
    else:
        with st.spinner("Reading CV and analyzing..."):
            summary = evaluate_cv(cv_content, jd_content)
        st.subheader("AI Match Summary")
        st.write(summary)

st.markdown("---")

user_q = st.text_area("Type any questions on CV", key="user_questions")

if cv_content:
    qa_chain = build_qa_chain(cv_content)

if user_q:
    answer = qa_chain({"query": user_q})
    st.write("🧠 Answer:", answer)
