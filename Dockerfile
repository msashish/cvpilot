FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install

COPY app .
COPY .env .

VOLUME ["/cv"]
VOLUME ["/jd"]

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "app/main.py"]
