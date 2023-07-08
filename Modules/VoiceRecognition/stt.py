from JZBot import dp, outpdir, GetChatStatus, GetBotLang, ReplyMsg, RundomName, DownloadFile, TextByLang
import speech_recognition as sr
from pydub import AudioSegment
from asyncer import asyncify

def stt_text(number):
    return TextByLang({
        'ru': [
            'Нужно ответить на сообщение которое содержит аудиофайл',
            'Размер аудиофайла не должен превышать 5мб',
            'Не удалось перевести голосовое сообщение в текст'
        ],
        'uk': [
            'Потрібно відповісти на повідомлення, яке містить аудіофайл',
            'Розмір аудіофайлу не повинен перевищувати 5мб',
            'Не вдалося перетворити аудіо на текст'
        ],
        'en': [
            'Reply to a message that contains an audio file',
            'The size of the audio file must not exceed 5MB',
            'Failed to convert audio to text'
        ]
    }, number)

def stt(audio_file, lang):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_text = r.listen(source)
        try:
            return r.recognize_google(audio_text, language=lang)
        except:
            return stt_text(2)

def ConvertAudio(InputFile, OutputFile, OutputFormat):
    return AudioSegment.from_file(InputFile).export(OutputFile, format=OutputFormat)

@dp.message_handler(commands=['stt'])
async def main_stt(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, stt_text(0))
        else:
            reply_msg = msg.reply_to_message
            audio_msg = reply_msg.voice if 'voice' in reply_msg else reply_msg.audio if 'audio' in reply_msg else None
            if audio_msg is not None:
                if audio_msg.file_size >= 5242880:
                    await ReplyMsg(msg, stt_text(1))
                else:
                    try:
                        file_id = audio_msg.file_id
                        file_format = audio_msg.mime_type.split('/')[1]
                        cmd_text = msg.text.split()
                        lang = cmd_text[1] if len(cmd_text) >= 2 else GetBotLang()
                        FileName = f'{outpdir}/{file_id}-{RundomName(10)}'
                        await DownloadFile(file_id, f'{FileName}.{file_format}')
                        if file_format != 'wav':
                            await asyncify(ConvertAudio)(f'{FileName}.{file_format}', f'{FileName}.wav', 'wav')
                            file_format = 'wav'
                        transcript = await asyncify(stt)(f'{FileName}.{file_format}', lang)
                        await ReplyMsg(msg, transcript)
                    except:
                        await ReplyMsg(msg, stt_text(2))
            else:
                await ReplyMsg(msg, stt_text(0))
