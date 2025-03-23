FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

EXPOSE 53533/udp

CMD ["python", "authoritative_server.py"]