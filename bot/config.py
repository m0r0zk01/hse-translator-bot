import os

TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
IAM_TOKEN = os.getenv('IAM_TOKEN')
FOLDER_ID = os.getenv('FOLDER_ID')

HELP_MESSAGE = '''
Hello!
This bot allows you to translate texts from any language to russian!

• /start or /help - see this message
• /ru - reply this to message to translate it to Russian
• /to-<lang_code> - reply this to message to translate it to any other language, specified by lang_code parameter. E.g. /to_en translates message to English
• /codes - get the language codes list
'''

LANGUAGE_CODES = '''
Check out [this Wikipedia article](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for available language codes\(639\-1 column of the table\)
'''
