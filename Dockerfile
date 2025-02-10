FROM python:3.12.4

ARG CLIENT_ID
ARG CLINET_SECRET
ARG API_KEY

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "main:app", "-b", "0.0.0.0:8000", "--chdir", "./app"]