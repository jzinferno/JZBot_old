from JZBot import dp, outpdir, GetBotLang, GetConfig, GetChatStatus, ReplyMsg, ReplyPhoto, DownloadFile, TextByLang, RundomName
from Modules.VoiceRecognition.stt import ConvertAudio
from pydub import AudioSegment
from asyncer import asyncify
from os import environ
import openai

openai.api_key = GetConfig('openai_key')

def openai_text(number):
    return TextByLang({
        'ru': [
            'Ваш запрос не может быть более 1000 символов',
            'Вы забыли ввести текст запроса',
            'Не удалось выполнить запрос OpenAi',
            'Нужно ответить на сообщение которое содержит аудиофайл',
            'Размер аудиофайла не должен превышать 1мб'
        ],
        'uk': [
            'Ваш запит не може бути більше ніж 1000 символів',
            'Ви забули ввести текст запиту',
            'Не вдалося виконати запит OpenAi',
            'Потрібно відповісти на повідомлення, яке містить аудіофайл',
            'Розмір аудіофайлу не повинен перевищувати 1мб'
        ],
        'en': [
            'Your request cannot be more than 1000 characters',
            'You forgot to enter the request text',
            'Failed to execute OpenAi request',
            'Reply to a message that contains an audio file',
            'The size of the audio file must not exceed 1MB'
        ]
    }, number)

@dp.message_handler(commands=['chat'])
async def main_chat(msg):
    if await GetChatStatus(msg) is not False:
        if len(msg.text) >= 1001:
            await ReplyMsg(msg, openai_text(0))
        else:
            if msg.text.find(' ') == -1:
                await ReplyMsg(msg, openai_text(1))
            else:
                try:
                    response = await openai.Completion.acreate(
                        model='text-davinci-003',
                        prompt=' '.join(msg.text.split()[1:]),
                        max_tokens=2400,
                        n=1
                    )
                    await ReplyMsg(msg, response.choices[0].text.strip())
                except:
                    await ReplyMsg(msg, openai_text(2))

@dp.message_handler(commands=['gpt'])
async def main_gpt(msg):
    if await GetChatStatus(msg) is not False:
        if len(msg.text) >= 1001:
            await ReplyMsg(msg, openai_text(0))
        else:
            if msg.text.find(' ') == -1:
                await ReplyMsg(msg, openai_text(1))
            else:
                try:
                    response = await openai.ChatCompletion.acreate(
                        model='gpt-3.5-turbo',
                        messages=[{
                            'role': 'user',
                            'content': ' '.join(msg.text.split()[1:])
                        }]
                    )
                    await ReplyMsg(msg, response.choices[0].message.content.strip())
                except:
                    await ReplyMsg(msg, openai_text(2))

@dp.message_handler(commands=['img'])
async def main_img(msg):
    if await GetChatStatus(msg) is not False:
        if msg.text.find(' ') == -1:
            await ReplyMsg(msg, openai_text(1))
        else:
            try:
                response = await openai.Image.acreate(
                    prompt=' '.join(msg.text.split()[1:]),
                    size='256x256',
                    n=1
                )
                await ReplyPhoto(msg, response.data[0].url, caption=' '.join(msg.text.split()[1:]))
            except:
                await ReplyMsg(msg, openai_text(2))

@dp.message_handler(commands=['wisper'])
async def main_wisper(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, openai_text(3))
        else:
            reply_msg = msg.reply_to_message
            audio_msg = reply_msg.voice if 'voice' in reply_msg else reply_msg.audio if 'audio' in reply_msg else None
            if audio_msg is not None:
                if audio_msg.file_size >= 1048577:
                    await ReplyMsg(msg, openai_text(4))
                else:
                    try:
                        file_id = audio_msg.file_id
                        file_format = audio_msg.mime_type.split('/')[1]
                        FileName = f'{outpdir}/{file_id}-{RundomName(10)}'
                        await DownloadFile(file_id, f'{FileName}.{file_format}')
                        if file_format == 'ogg':
                            await asyncify(ConvertAudio)(f'{FileName}.{file_format}', f'{FileName}.wav', 'wav')
                            file_format = 'wav'
                        transcript = await openai.Audio.atranscribe('whisper-1', open(f'{FileName}.{file_format}', 'rb'))
                        await ReplyMsg(msg, transcript.text.strip())
                    except:
                        await ReplyMsg(msg, openai_text(2))
            else:
                await ReplyMsg(msg, openai_text(3))
