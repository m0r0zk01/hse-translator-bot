from aiogram import Bot, Dispatcher, executor, types, filters
import logging
import psycopg2

from random import randint
import config
import ya_translator_api

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TG_BOT_TOKEN)
dp = Dispatcher(bot)

api = ya_translator_api.YaTranslatorApi()

conn = psycopg2.connect(
    database = "db",
    user = "postgres",
    password ="postgres",
    port = "5432",
    host = "db"
)

cur = conn.cursor()

@dp.message_handler(commands=['start', 'help'])
async def help(message: types.Message):
    await message.reply(config.HELP_MESSAGE)

@dp.message_handler(commands=['codes'])
async def codes(message: types.Message):
    await message.reply(config.LANGUAGE_CODES, parse_mode='MarkdownV2', disable_web_page_preview=True)

async def process_translation(message: types.Message):
    reply = message.reply_to_message
    if reply is None:
        await message.reply('Please, reply to message with text')
        return None

    target_lang_code = 'ru'
    if message.get_command().startswith('/to-'):
        target_lang_code = message.get_command()[4:]   # trim '/to_'

    translation = await api.translate(text=reply.text, target_lang=target_lang_code, source_lang=None)
    if translation.get('code', 0) != 0:
        await message.reply(translation.get('message', 'something went wrong:/'))
        return None

    translations = translation.get('translations', [])
    if type(translations) != list or len(translations) == 0:
        await message.reply('something went wrong:/')
        return None

    if (translated_text := translations[0].get('text', None)) is None:
        await message.reply('something went wrong:/')
        return None
    return translated_text

@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['ru', 'to-([a-z]{1,3})']))
async def translate(message: types.Message):
    translated_text = await process_translation(message)
    await message.reply(translated_text)

@dp.message_handler(commands=['save'])
async def save(message: types.Message):
    reply = message.reply_to_message
    if reply is None:
        await message.reply('Please, reply to message with text')
        return

    translated_text = await process_translation(message)
    if reply.text is None or translated_text is None:
        await message.reply('something went wrong:/')
        return

    cur.execute('''
        INSERT INTO texts (user_id, initial_text, translated_text) VALUES (%s, %s, %s);
    ''', (message.from_user.id, reply.text, translated_text, ))
    conn.commit()

    await message.reply('Done!')

def quote_tags(text):
    return text.replace('<', '\<').replace('>', '\>')

@dp.message_handler(commands=['list'])
async def save(message: types.Message):
    cur.execute(f'''
        SELECT * FROM texts WHERE user_id=%s;
    ''', (message.from_user.id, ))
    result = cur.fetchall()

    reply_text = 'Your list:\n\n' if len(result) != 0 else 'Your list is empty:( Reply /save to some text to save it'
    for i, row in enumerate(result):
        reply_text += f'{i}. {quote_tags(row[2])} - <span class="tg-spoiler">{quote_tags(row[3])}</span>\n'
    await message.reply(reply_text, parse_mode='HTML')

@dp.message_handler(commands=['rand'])
async def rand(message: types.Message):
    cur.execute(f'''
        SELECT * FROM texts WHERE user_id=%s;
    ''', (message.from_user.id, ))
    result = cur.fetchall()

    if len(result) == 0:
        await message.reply('Your list is empty:( Reply /save to some text to save it')
        return
    
    reply_text = 'Your random phrase:\n'
    ind = randint(0, len(result) - 1)
    reply_text += f'{quote_tags(result[ind][2])} - <span class="tg-spoiler">{quote_tags(result[ind][3])}</span>\n'
    await message.reply(reply_text, parse_mode='HTML')

@dp.message_handler(commands=['delete'])
async def delete(message: types.Message):
    splitted = message.text.split()
    if len(splitted) == 1:
        await message.reply('No index provided:( Please type /delete <index to delete>')
        return
    
    ind: str = splitted[1]
    if not ind.isdecimal():
        await message.reply('Index should be an integer')
        return
    ind = int(ind)

    cur.execute(f'''
        SELECT * FROM texts WHERE user_id=%s;
    ''', (message.from_user.id, ))
    result = cur.fetchall()


    if not 0 <= ind < len(result):
        await message.reply('Wrong index')
        return

    cur.execute(f'''
        DELETE FROM texts WHERE id=%s;
    ''', (result[ind][0], ))
    
    conn.commit()
    await message.reply('Done!')

def db_init():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS texts (id serial PRIMARY KEY, user_id integer, initial_text text, translated_text text);
    ''')

if __name__ == '__main__':
    db_init()
    executor.start_polling(dp, skip_updates=True)
