from JZBot import dp, GetBotLang, GetChatStatus, ReplyMsg, TextByLang
from gpytranslate import Translator
import aiofiles

def translate_text(text):
    return TextByLang({
        'ru': {
            'text_1': 'Нужно ответить на сообщение или ввести текст',
            'text_2': 'Не удалось перевести текст',
            'text_3': 'Не удалось определить язык текста'
        },
        'uk': {
            'text_1': 'Потрібно відповісти на повідомлення чи ввести текст',
            'text_2': 'Не вдалося перекласти текст',
            'text_3': 'Не вдалося визначити мову тексту'
        },
        'en': {
            'text_1': 'Reply to a message or enter text',
            'text_2': 'Failed to translate text',
            'text_3': 'Failed to determine text language'
        }
    }, text)

@dp.message_handler(commands=['translate'])
async def main_translate(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' in msg:
            text = msg.reply_to_message.text
        else:
            text = ' '.join(msg.text.split()[1:])
        if text == '':
            await ReplyMsg(msg, translate_text('text_1'))
        else:
            try:
                translator = Translator()
                result = await translator.translate(text, targetlang=GetBotLang())
                await ReplyMsg(msg, result.text)
            except:
                await ReplyMsg(msg, translate_text('text_2'))

@dp.message_handler(commands=['lang'])
async def main_lang(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' in msg:
            text = msg.reply_to_message.text
        else:
            text = ' '.join(msg.text.split()[1:])
        if text == '':
            await ReplyMsg(msg, translate_text('text_1'))
        else:
            try:
                translator = Translator()
                await ReplyMsg(msg, await translator.detect(text))
            except:
                await ReplyMsg(msg, translate_text('text_3'))
