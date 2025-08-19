from gemini_agent import evaluate_cv

#from agents.chatopenai_agent import evaluate_cv
from utils import extract_text_from_file

resume_path = "cv/AshwiniSwamy_SeniorEngineer_Fractal.pdf"
jd_path = "jd/sr_cloud_engineer.txt"

print(f"Will evaluate CV {resume_path} against JD {jd_path} ")

# Get JD text
jd_text = extract_text_from_file(jd_path)
print("Extracted JD content for reference")

# Get CV text
resume_text = extract_text_from_file(resume_path)
print("Extracted CV content for evaluation")

summary = evaluate_cv(resume_text, jd_text)
print(summary)
