FROM python:3.12-slim-bookworm

COPY ./engine /app
COPY ./requirements.txt /app 

WORKDIR /app
RUN mkdir /picoci
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
