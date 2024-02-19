import os


# ChatGPT
OPENAI_MODEL = 'gpt-3.5-turbo'
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')

# RabbitMQ
RABBITMQ_URL = 'amqp://guest:guest@172.24.60.254:5672/'
# RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672/'
# RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/'
TO_CHAT_GPT_QUEUE = 'to_chat_gpt_queue'
FROM_CHAT_GPT_QUEUE = 'from_chat_gpt_queue'
