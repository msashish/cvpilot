# cvpilot

        AI copilot for CV/resume evaluations like a bird on LinkedIn
        — just trying to land the perfect job without ruffling too many feathers

## Basic App

### How to run ?

        Basic App uses Google's Gemini as it has good free tier options https://ai.google.dev/gemini-api/docs/rate-limits#free-tier

        Step1: Generate API key from https://aistudio.google.com/app/apikey
                and set it in basic_app/.env

        Step2: Pick a model from https://ai.google.dev/gemini-api/docs/rate-limits#free-tier
                and configure it at basic_app/gemini_agent.py 

        Step3: Install required libraries
                If you have virtual env then make sure to use "poetry env use"
                poetry install

        Step4: Test your code
                python basic_app/main.py

### Basic App flow

    [User Uploads Resume PDF/DOCX]
            ↓
    [Resume Extraction]
            ↓
    [JD Extraction]
            ↓
    [Agent (Gemini / LangChain / CrewAI)]
            ↓
    - Loads JD
    - Compares skills, roles, certs, etc.
    - Summarizes match/gaps
            ↓
    [Response Returned to User]

## Full App

        UI

### How to build ?

        docker build . -t cvpilot-app
        docker run -v /Users/sheelava/msashishgit/cvpilot/jd:jd -v /Users/sheelava/msashishgit/cvpilot/cv:cv cvpilot-app

### How to use ?

        python basic_app/main.py
        python
        poetry install
        poetry run streamlit run app/main.py

### Tech Stack

| Feature              | Tool                                        |
| -------------------- | ------------------------------------------- |
| Resume Parsing       | `pdfplumber`, `python-docx`, `unstructured` |
| LLM                  | Gemini LLM /OpenAI GPT / Vertex AI (GCP)    |
| Agentic Framework    | `LangChain` or `CrewAI`                     |
| Optionally Deploy UI | Streamlit / Flask                           |


## Extras

        streamlit helps convert raw data into visual delight - tables, histogram etc
                https://docs.streamlit.io/
                https://docs.streamlit.io/get-started/tutorials/create-an-app

        streamlit run pick.py  

