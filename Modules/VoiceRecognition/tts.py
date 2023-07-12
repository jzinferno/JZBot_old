from JZBot import dp, outpdir, GetChatStatus, ReplyMsg, RundomName, ReplyVoice, RunShellCmd, TextByLang, Message
from gpytranslate import Translator

def tts_text(number):
    return TextByLang({
        'ru': [
            'Нужно ответить на сообщение или ввести текст',
            'Не удалось озвучить текст'
        ],
        'uk': [
            'Потрібно відповісти на повідомлення чи ввести текст',
            'Не вдалося озвучити текст'
        ],
        'en': [
            'Reply to a message or enter text',
            'Failed to speak text'
        ]
    }, number)

@dp.message_handler(commands=['tts'])
async def main_tts(msg: Message):
    if await GetChatStatus(msg) is not False:
        try:
            translator = Translator()
            text = msg.reply_to_message.text if 'reply_to_message' in msg else ' '.join(msg.text.split()[1:])
            if text == '':
                await ReplyMsg(msg, tts_text(0))
            else:
                file_name = outpdir + '/tts-' + RundomName(10) + '.mp3'
                await RunShellCmd(f'gtts-cli -l {await translator.detect(text)} \'{text}\' -o {file_name}')
                await ReplyVoice(msg, open(file_name, 'rb'))
        except:
            await ReplyMsg(msg, tts_text(1))
