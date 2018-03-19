FROM python:alpine3.6

WORKDIR /src
COPY . .

RUN ["pip3", "install", "-r", "requirements.txt"]

EXPOSE 5400

ENTRYPOINT ["python3", "-u", "main.py"]
