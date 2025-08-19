from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI


def evaluate_cv(resume_text, jd_text):


    # Create a LangChain Prompt Template  
    prompt = PromptTemplate.from_template("""
You are a hiring for ANZ. Evaluate this resume against the JD.

### JOB DESCRIPTION:
{jd}

### RESUME:
{resume}

Give:
- Suitability Score (/10)
- Matching Skills
- Missing Skills
- Recommendation
""")

    # Set up LLMChain
    llm = OpenAI(temperature=0)
    chain = prompt | llm
    return chain.invoke({"jd": jd_text, "resume": resume_text})
