FROM python:3.12

RUN apt-get update && apt-get install -y iproute2

RUN pip install aio-pika aiohttp openai

COPY src /app
WORKDIR /app

CMD ["python", "/app/app.py"]