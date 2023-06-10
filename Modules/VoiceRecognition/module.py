from JZBot import dp, bot, GetChatStatus, GetBotLang, outpdir, ReplyMsg, RundomName, ReplyVoice, RunShellCmd, DownloadFile, TextByLang
import speech_recognition as sr
from pydub import AudioSegment
from asyncer import asyncify
from gpytranslate import Translator

def stt_text(text):
    return TextByLang({
        'ru': {
            'text_1': 'Нужно ответить на сообщение которое содержит аудиофайл',
            'text_2': 'Размер аудиофайла не должен превышать 5мб',
            'text_3': 'Не удалось перевести голосовое сообщение в текст'
        },
        'uk': {
            'text_1': 'Потрібно відповісти на повідомлення, яке містить аудіофайл',
            'text_2': 'Розмір аудіофайлу не повинен перевищувати 5мб',
            'text_3': 'Не вдалося перетворити аудіо на текст'
        },
        'en': {
            'text_1': 'Reply to a message that contains an audio file',
            'text_2': 'The size of the audio file must not exceed 5MB',
            'text_3': 'Failed to convert audio to text'
        }
    }, text)

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

def stt(audio_file, lang):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_text = r.listen(source)
        try:
            return r.recognize_google(audio_text, language=lang)
        except:
            return stt_text('text_3')

def ConvertAudio(InputFile, OutputFile, OutputFormat):
    return AudioSegment.from_file(InputFile).export(OutputFile, format=OutputFormat)

@dp.message_handler(commands=['stt'])
async def main_stt(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, stt_text('text_1'))
        else:
            reply_msg = msg.reply_to_message
            audio_msg = reply_msg.voice if 'voice' in reply_msg else reply_msg.audio if 'audio' in reply_msg else None
            if audio_msg is not None:
                if audio_msg.file_size >= 5242880:
                    await ReplyMsg(msg, stt_text('text_2'))
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
                        await ReplyMsg(msg, stt_text('text_3'))
            else:
                await ReplyMsg(msg, stt_text('text_1'))

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
