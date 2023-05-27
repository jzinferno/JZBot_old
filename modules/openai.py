from main import dp, bot, outpdir, GetBotLang, GetConfig, GetChatStatus
from pydub import AudioSegment
from JZBot import JZBot
from os import environ
import openai

openai.api_key = GetConfig('openai_key')

def openai_text(text):
    full_text = {
        'ru': {
            'text_1': 'Ваш запрос не может быть более 1000 символов',
            'text_2': 'Вы забыли ввести текст запроса',
            'text_3': 'Не удалось выполнить запрос OpenAi',
            'text_4': 'Нужно ответить на сообщение которое содержит аудиофайл',
            'text_5': 'Размер аудиофайла не должен превышать 1мб'
        },
        'uk': {
            'text_1': 'Ваш запит не може бути більше ніж 1000 символів',
            'text_2': 'Ви забули ввести текст запиту',
            'text_3': 'Не вдалося виконати запит OpenAi',
            'text_4': 'Потрібно відповісти на повідомлення, яке містить аудіофайл',
            'text_5': 'Розмір аудіофайлу не повинен перевищувати 1мб'
        },
        'en': {
            'text_1': 'Your request cannot be more than 1000 characters',
            'text_2': 'You forgot to enter the request text',
            'text_3': 'Failed to execute OpenAi request',
            'text_4': 'Reply to a message that contains an audio file',
            'text_5': 'The size of the audio file must not exceed 1MB'
        }
    }
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

@dp.message_handler(commands=['chat'])
async def main_chat(msg):
    if await GetChatStatus(msg) is not False:
        if len(msg.text) >= 1001:
            await JZBot.ReplyMsg(msg, openai_text('text_1'))
        else:
            if msg.text.find(' ') == -1:
                await JZBot.ReplyMsg(msg, openai_text('text_2'))
            else:
                try:
                    response = await openai.Completion.acreate(
                        model='text-davinci-003',
                        prompt=' '.join(msg.text.split()[1:]),
                        max_tokens=2400,
                        n=1
                    )
                    await JZBot.ReplyMsg(msg, response.choices[0].text.strip())
                except:
                    await JZBot.ReplyMsg(msg, openai_text('text_3'))

@dp.message_handler(commands=['gpt'])
async def main_gpt(msg):
    if await GetChatStatus(msg) is not False:
        if len(msg.text) >= 1001:
            await JZBot.ReplyMsg(msg, openai_text('text_1'))
        else:
            if msg.text.find(' ') == -1:
                await JZBot.ReplyMsg(msg, openai_text('text_2'))
            else:
                try:
                    response = await openai.ChatCompletion.acreate(
                        model='gpt-3.5-turbo',
                        messages=[{
                            'role': 'user',
                            'content': ' '.join(msg.text.split()[1:])
                        }]
                    )
                    await JZBot.ReplyMsg(msg, response.choices[0].message.content.strip())
                except:
                    await JZBot.ReplyMsg(msg, openai_text('text_3'))

@dp.message_handler(commands=['img'])
async def main_img(msg):
    if await GetChatStatus(msg) is not False:
        if msg.text.find(' ') == -1:
            await JZBot.ReplyMsg(msg, openai_text('text_2'))
        else:
            try:
                response = await openai.Image.acreate(
                    prompt=' '.join(msg.text.split()[1:]),
                    size='256x256',
                    n=1
                )
                await JZBot.ReplyPhoto(msg, response.data[0].url, caption=' '.join(msg.text.split()[1:]))
            except:
                await JZBot.ReplyMsg(msg, openai_text('text_3'))

@dp.message_handler(commands=['wisper'])
async def main_wisper(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await JZBot.ReplyMsg(msg, openai_text('text_4'))
        else:
            reply_msg = msg.reply_to_message
            audio_msg = reply_msg.voice if 'voice' in reply_msg else reply_msg.audio if 'audio' in reply_msg else None
            if audio_msg is not None:
                if audio_msg.file_size >= 1048577:
                    await JZBot.ReplyMsg(msg, openai_text('text_5'))
                else:
                    try:
                        file_id = audio_msg.file_id
                        file_format = audio_msg.mime_type.split('/')[1]
                        await bot.download_file((await bot.get_file(file_id)).file_path, f'{outpdir}/{file_id}.{file_format}')
                        if file_format == 'ogg':
                            AudioSegment.from_file(f'{outpdir}/{file_id}.{file_format}').export(f'{outpdir}/{file_id}.wav', format='wav')
                            file_format = 'wav'
                        transcript = await openai.Audio.atranscribe('whisper-1', open(f'{outpdir}/{file_id}.{file_format}', 'rb'))
                        await JZBot.ReplyMsg(msg, transcript.text.strip())
                    except:
                        await JZBot.ReplyMsg(msg, openai_text('text_3'))
            else:
                await JZBot.ReplyMsg(msg, openai_text('text_4'))