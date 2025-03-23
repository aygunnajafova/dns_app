FROM python:3.9-slim

RUN pip install Flask requests

WORKDIR /usr/src/app

COPY . .

EXPOSE 8080

CMD ["python", "user_server.py"]