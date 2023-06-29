FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY similarity_scores.pkl .
COPY books.pkl .
COPY final.pkl .
COPY pt.pkl .

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--port", "80"]
