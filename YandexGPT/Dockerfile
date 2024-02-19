FROM python:3.12

RUN pip install aio-pika aiohttp

COPY src /app

WORKDIR /app

# Запускаем микросервис
CMD ["python", "app.py"]
