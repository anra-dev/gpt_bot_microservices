from enum import Enum


class ModelGPTEnumForBD(Enum):

    CHATGPT = 'chatgpt'
    YANDEXGPT = 'yandexgpt'


class ModelGPTEnum(Enum):

    CHATGPT = 'chatgpt'
    YANDEXGPT = 'yandexgpt'

    DEFAULT_SYSTEM_ROLE = {
        CHATGPT: 'You’re a kind helpful assistant. Your name John.',
        YANDEXGPT: 'Ты умный ассистент. Тебя зовут Алиса.',
    }

    CONTENT_KEY = {
        CHATGPT: 'content',
        YANDEXGPT: 'text',
    }
