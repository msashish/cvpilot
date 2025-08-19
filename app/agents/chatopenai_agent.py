import os

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# --- Optional: set your API key (or export as ENV var OPENAI_API_KEY)

def evaluate_cv(cv_text, jd_text):
    # --- Step 2: Create a LangChain Prompt Template ---
    prompt = PromptTemplate(
        input_variables=["jd", "cv"],
        template="""
    You are an AI expert assessing CVs.

    Given this job description:
    "{jd}"

    And this resume:
    "{cv}"

    Provide:
    1. A suitability score (1 to 10)
    2. 3–5 bullet points on the strengths and weaknesses of this candidate
    3. Recommendation: Should this candidate be shortlisted? (Yes/No with reason)
    """
    )

    # --- Step 3: Set up LLMChain ---
    llm = ChatOpenAI(temperature=0.2, model_name="gpt-4")  # or gpt-3.5-turbo
    chain = LLMChain(llm=llm, prompt=prompt)

    # --- Step 4: Run the Chain ---
    result = chain.run(jd=jd_text, cv=cv_text)

    # --- Step 5: Print the Output ---
    #print(result)
    return result
