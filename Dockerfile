FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

LABEL maintainer="Micael de Prado <micael.deprado@gmail.com>"

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY ./app /app