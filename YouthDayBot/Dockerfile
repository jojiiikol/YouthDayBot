FROM python:3.12.4

ENV TZ="Asia/Yekaterinburg"

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
