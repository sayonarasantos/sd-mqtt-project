FROM python:3.11-slim-bullseye

WORKDIR /project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]