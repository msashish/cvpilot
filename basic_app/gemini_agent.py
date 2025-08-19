import google.generativeai as genai
from config import GEMINI_API_KEY

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
