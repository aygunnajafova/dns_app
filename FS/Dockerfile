FROM python:3.9-slim

RUN pip install Flask requests

WORKDIR /usr/src/app

COPY . .

EXPOSE 9090

CMD ["python", "fibonacci_server.py"]