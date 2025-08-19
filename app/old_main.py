import streamlit as st
from core import build_qa_chain
from gemini_agent import evaluate_cv
from utils import load_pdf, load_webpage

st.title("📄🔍 CV Assistant AI")

# Initialize the key in session state if not present
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

cv_source = st.radio("Choose your CV format", ["PDF", "Web Page"])
cv_content = []
if cv_source == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf", key="cv_uploader")
    if uploaded_file:
        cv_content = load_pdf(uploaded_file)
elif cv_source == "Web Page":
    url = st.text_input("Enter a URL")
    if url:
        cv_content = load_webpage(url)

jd_source = st.radio("Choose your JD format", ["PDF", "Text", "Web Page"])
jd_content = []
if jd_source == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf", key="jd_uploader")
    if uploaded_file:
        jd_content = load_pdf(uploaded_file)
elif jd_source == "Web Page":
    url = st.text_input("Enter a URL")
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

if st.button("Need more clarifications"):
    chain = build_qa_chain(cv_content)
    user_q = st.text_input("Ask a question about the CV:")
    if user_q:
        answer = chain.run(user_q)
        st.write("🧠 Answer:", answer)
