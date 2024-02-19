import asyncio
import json

import aio_pika

import settings
from api import save_answer
from models import Message


async def publish(queue_name, data, message_id) -> None:
    connection = await aio_pika.connect_robust(url=settings.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        data = json.dumps(data)
        queue = await channel.declare_queue(queue_name, auto_delete=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=data.encode(), message_id=message_id), routing_key=queue.name)


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    from main import send_message_by_chat_id

    answer = message.body.decode()
    message_obj: Message = save_answer(message_id=message.message_id, answer=answer)

    async with message.process():
        # telegram.error.BadRequest: Message is too long
        await send_message_by_chat_id(
            message=message.body.decode(),
            chat_id=message_obj.context.user.chat_id,
            model=message_obj.context.user.model.value,
        )


async def consume(queue_name) -> None:
    await asyncio.sleep(10)  # Ждем RabbitMQ
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(name=queue_name, auto_delete=True)
    await queue.consume(process_message)

    try:
        print(f'Listening to queue: {queue_name}')
        await asyncio.Future()
    finally:
        await connection.close()
