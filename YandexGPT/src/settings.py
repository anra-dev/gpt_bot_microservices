import os


# Yandex
YANDEX_URL = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
YANDEX_URL_RESULT = 'https://llm.api.cloud.yandex.net/operations/'
YANDEX_DIR_ID = os.environ.get('YANDEX_DIR_ID')
YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY')
TIMEOUT_API_YANDEX = 1

# RabbitMQ
RABBITMQ_URL = 'amqp://guest:guest@rabbitmq:5672/'
TO_YANDEX_GPT_QUEUE = 'to_yandex_gpt_queue'
FROM_YANDEX_GPT_QUEUE = 'from_yandex_gpt_queue'
