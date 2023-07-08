from JZBot import dp, GetBotLang, GetChatStatus, ReplyMsg, TextByLang
from gpytranslate import Translator
import aiofiles

def translate_text(number):
    return TextByLang({
        'ru': [
            'Нужно ответить на сообщение или ввести текст',
            'Не удалось перевести текст',
            'Не удалось определить язык текста'
        ],
        'uk': [
            'Потрібно відповісти на повідомлення чи ввести текст',
            'Не вдалося перекласти текст',
            'Не вдалося визначити мову тексту'
        ],
        'en': [
            'Reply to a message or enter text',
            'Failed to translate text',
            'Failed to determine text language'
        ]
    }, number)

@dp.message_handler(commands=['translate'])
async def main_translate(msg):
    if await GetChatStatus(msg) is not False:
        cmd = msg.text.split()
        if 'reply_to_message' in msg:
            text = msg.reply_to_message.text
            lang = cmd[1] if len(cmd) >= 2 else GetBotLang()
        else:
            text = ' '.join(cmd[1:])
            lang = GetBotLang()
        if text == '':
            await ReplyMsg(msg, translate_text(0))
        else:
            try:
                translator = Translator()
                result = await translator.translate(text, targetlang=lang)
                await ReplyMsg(msg, result.text)
            except:
                await ReplyMsg(msg, translate_text(1))

@dp.message_handler(commands=['lang'])
async def main_lang(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' in msg:
            text = msg.reply_to_message.text
        else:
            text = ' '.join(msg.text.split()[1:])
        if text == '':
            await ReplyMsg(msg, translate_text(0))
        else:
            try:
                translator = Translator()
                await ReplyMsg(msg, await translator.detect(text))
            except:
                await ReplyMsg(msg, translate_text(2))
