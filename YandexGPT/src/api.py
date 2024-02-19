import asyncio
import json
import aiohttp

import settings
from logger import logger


dir_id = settings.YANDEX_DIR_ID
API_KEY = settings.YANDEX_API_KEY

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Api-Key {API_KEY}'
}

headers_result = {
    'Content-Type': 'application/json',
    'Authorization': f'Api-Key {API_KEY}'
}


async def get_result(operation_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=settings.YANDEX_URL_RESULT + operation_id,
                headers=headers_result,
                verify_ssl=False
        ) as response:
            response_json = await response.json()
            try:
                answer = response_json['response']['alternatives'][0]['message']['text']
            except KeyError:
                error = response_json.get('error')
                if not error:
                    await asyncio.sleep(settings.TIMEOUT_API_YANDEX)
                    answer = await get_result(operation_id)
                else:
                    logger.error(response_json)
                    answer = error
            return answer


async def async_request(messages):
    prompt = {
        'modelUri': f'gpt://{dir_id}/yandexgpt-lite',
        'completionOptions': {
            'stream': False,
            'temperature': 0.5,
            'maxTokens': 2000,
        },
        'messages': messages,
    }
    data = json.dumps(prompt, ensure_ascii=False).encode("utf8")
    async with aiohttp.ClientSession() as session:

        async with session.post(url=settings.YANDEX_URL, headers=headers, data=data, verify_ssl=False) as response:
            status_code = response.status
            if status_code == 200:
                response_json = await response.json()
                operation_id = response_json.get('id')
                return await get_result(operation_id)
            else:
                return f'Status code{status_code}, text: {response.text}'
