FROM python:3.11-slim-bullseye

WORKDIR /project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

WORKDIR /project/app

CMD ["python", "main.py"]