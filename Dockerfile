FROM python:3.11-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /WebApp
WORKDIR /WebApp
COPY req.txt .
RUN pip3 install -r req.txt

COPY . /WebApp

CMD uvicorn main:app --port 8001 --host 0.0.0.0