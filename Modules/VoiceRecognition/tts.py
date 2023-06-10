from JZBot import dp, outpdir, GetChatStatus, ReplyMsg, RundomName, ReplyVoice, RunShellCmd, TextByLang
from gpytranslate import Translator

def tts_text(text):
    return TextByLang({
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
    }, text)

@dp.message_handler(commands=['tts'])
async def main_tts(msg):
    if await GetChatStatus(msg) is not False:
        try:
            translator = Translator()
            text = msg.reply_to_message.text if 'reply_to_message' in msg else ' '.join(msg.text.split()[1:])
            if text == '':
                await ReplyMsg(msg, tts_text('text_1'))
            else:
                file_name = outpdir + '/tts-' + RundomName(10) + '.mp3'
                await RunShellCmd(f'gtts-cli -l {await translator.detect(text)} \'{text}\' -o {file_name}')
                await ReplyVoice(msg, open(file_name, 'rb'))
        except:
            await ReplyMsg(msg, tts_text('text_2'))
