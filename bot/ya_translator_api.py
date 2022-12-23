import aiohttp

import config

class YaTranslatorApi:
    def __init__(self):
        self.data = {
            "sourceLanguageCode": "",   # need to fill
            "targetLanguageCode": "",   # need to fill
            "texts": [
                # need to fill
            ],
            "folderId": f"{config.FOLDER_ID}",
        }
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.IAM_TOKEN}"
        }
        self.session = aiohttp.ClientSession('https://translate.api.cloud.yandex.net/')

    async def translate(self, text, target_lang='ru', source_lang=None):
        self.data['texts'] = [text]
        self.data['targetLanguageCode'] = target_lang
        self.data['sourceLanguageCode'] = source_lang

        async with self.session.post('/translate/v2/translate', json=self.data, headers=self.headers) as response:
            return await response.json()
