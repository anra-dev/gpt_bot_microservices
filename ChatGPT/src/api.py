import openai
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

import settings


client = AsyncOpenAI(api_key=settings.OPENAI_TOKEN)

openai.api_key = settings.OPENAI_TOKEN
LENGTH_EXCEEDED_TEXT = '🤖Превышена длинна контекста. Очистите контекст или удалите часть сообщений.'
LENGTH_EXCEEDED_CODE = 'context_length_exceeded'


async def async_request(messages):

    try:
        completion = await client.chat.completions.create(
            messages=messages,
            model=settings.OPENAI_MODEL,
        )
        answer = completion.choices[0].message.content
    except openai.OpenAIError as e:
        # if e.code == LENGTH_EXCEEDED_CODE:
        #     answer = LENGTH_EXCEEDED_TEXT
        # else:
        #     answer = str(e)
        answer = str(e)
    return answer
