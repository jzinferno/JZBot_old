from JZBot import dp, GetChatStatus, GetBotLang, outpdir, ReplyMsg, RundomName, ReplyVoice
from gpytranslate import Translator
from pydub import AudioSegment
from aiogtts import aiogTTS

def tts_text(text):
    full_text = {
        'ru': {
            'text_1': 'Нужно ответить на сообщение или ввести текст',
            'text_2': 'Не удалось озвучить текст'
        },
        'uk': {
            'text_1': 'Потрібно відповісти на повідомлення чи ввести текст',
            'text_2': 'Не вдалося озвучити текст'
        },
        'en': {
            'text_1': 'Reply to a message or enter text',
            'text_2': 'Failed to speak text'
        }
    }
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

@dp.message_handler(commands=['tts'])
async def main_tts(msg):
    if await GetChatStatus(msg) is not False:
        try:
            aiogtts = aiogTTS()
            translator = Translator()
            text = msg.reply_to_message.text if 'reply_to_message' in msg else ' '.join(msg.text.split()[1:])
            if text == '':
                await ReplyMsg(msg, tts_text('text_1'))
            else:
                file_name = outpdir + '/tts-' + RundomName(10)
                await aiogtts.save(text, f'{file_name}.mp3', lang=await translator.detect(text))

                AudioSegment.from_file(f'{file_name}.mp3').export(f'{file_name}.ogg', format='ogg')
                await ReplyVoice(msg, open(f'{file_name}.ogg', 'rb'))
        except:
            await ReplyMsg(msg, tts_text('text_2'))
