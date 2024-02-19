import asyncio
import json

import aio_pika

import settings
import api
from logger import logger


async def publish(data, message_id) -> None:
    connection = await aio_pika.connect_robust(url=settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(settings.FROM_CHAT_GPT_QUEUE, auto_delete=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=data.encode(), message_id=message_id),
            routing_key=queue.name,
        )


async def process_message(message: aio_pika.abc.AbstractIncomingMessage,) -> None:
    async with message.process():
        data = json.loads(message.body.decode())
        logger.info(f'Запрос: {data}')
        answer = await api.async_request(messages=data)
        logger.info(f'Ответ: {answer}')
        await publish(data=answer, message_id=message.message_id)


async def consume() -> None:
    await asyncio.sleep(15)  # Ждем RabbitMQ
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(settings.TO_CHAT_GPT_QUEUE, auto_delete=True)
    await queue.consume(process_message)

    try:
        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    print('test')
    asyncio.run(consume())
