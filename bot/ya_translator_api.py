import aiohttp
import sys
import time

import config

class YaTranslatorApi:
    def __init__(self):
        self.data = {
            'sourceLanguageCode': '',   # need to fill
            'targetLanguageCode': '',   # need to fill
            'texts': [
                # need to fill
            ],
            'folderId': f'{config.FOLDER_ID}',
        }
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': '',    # need to fill
        }
        self.session = aiohttp.ClientSession('https://translate.api.cloud.yandex.net/')
        self.last_token_update_time = 0
        self.token_lifetime_seconds = 1000 - 7

    async def translate(self, text, target_lang='ru', source_lang=None):
        if time.time() - self.last_token_update_time > self.token_lifetime_seconds:
            self.last_token_update_time = time.time()
            await config.update_iam_token()
        self.data['texts'] = [text]
        self.data['targetLanguageCode'] = target_lang
        self.data['sourceLanguageCode'] = source_lang
        self.headers['Authorization'] = f'Bearer {config.IAM_TOKEN}'

        async with self.session.post('/translate/v2/translate', json=self.data, headers=self.headers) as response:
            return await response.json()
