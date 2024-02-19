import os

from enums import ModelGPTEnumForBD

# Database
DATABASE = 'sqlite:///chatgpt.db'

# Telegram
BOT_VERSION = '1.6'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
DEFAULT_MODEL = ModelGPTEnumForBD.YANDEXGPT
SAFEGUARD_PHRASE = os.environ.get('SAFEGUARD_PHRASE')
SENDING_INTERVAL = 5

# ChatGPT
OPENAI_MODEL = 'gpt-3.5-turbo'
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')

# Yandex
YANDEX_DIR_ID = os.environ.get('YANDEX_DIR_ID')
YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY')
TIMEOUT_API_YANDEX = 1

# RabbitMQ
RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672/'
TO_CHAT_GPT_QUEUE = 'to_chat_gpt_queue'
FROM_CHAT_GPT_QUEUE = 'from_chat_gpt_queue'
TO_YANDEX_GPT_QUEUE = 'to_yandex_gpt_queue'
FROM_YANDEX_GPT_QUEUE = 'from_yandex_gpt_queue'
