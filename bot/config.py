import os
import aiohttp

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
YA_OAUTH_TOKEN = os.getenv('YA_OAUTH_TOKEN')
IAM_TOKEN = ''
FOLDER_ID = os.getenv('FOLDER_ID')

async def update_iam_token():
    global IAM_TOKEN
    async with aiohttp.ClientSession() as session:
        async with session.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', json={"yandexPassportOauthToken": YA_OAUTH_TOKEN}) as response:
            IAM_TOKEN = (await response.json())['iamToken']

HELP_MESSAGE = '''
Hello!

This bot allows you to translate texts from any language to Russian and vice versa:
• /start or /help - see this message
• /ru - reply this to message to translate it to Russian
• /to-[lang_code] - reply this to message to translate it to any other language, specified by lang_code parameter. E.g. /to_en translates message to English
• /codes - get the list of supported language codes

You can also save any phrase and its translation to your list:
• /save - reply this to message to save text to your list
• /list - display your list
• /rand - get random phrase and its spoilered translation
• /delete [index] - delete phrase from list by its index(taken from /list command)
'''

LANGUAGE_CODES = '''
Check out [this Wikipedia article](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for available language codes\(639\-1 column of the table\)
'''
