FROM python:3.12.4

ARG CLIENT_ID
ARG CLIENT_SECRET
ARG API_KEY

ENV CLIENT_ID=${CLIENT_ID}
ENV CLIENT_SECRET=${CLIENT_SECRET}
ENV API_KEY=${API_KEY}

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "main:app", "--chdir", "./app"]