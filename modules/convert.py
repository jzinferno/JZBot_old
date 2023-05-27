from main import dp, bot, GetBotLang, GetChatStatus, outpdir
from aiogram.types import InputFile
from pydub import AudioSegment
from JZBot import JZBot
from PIL import Image

def convert_text(text):
    full_text = {
        'ru': {
            'text_1': 'Необходимо ответить на сообщение которое содержит изображение',
            'text_2': 'Не удалось отредактировать фото'
        },
        'uk': {
            'text_1': 'Необходимо ответить на сообщение которое содержит изображение',
            'text_2': 'Не удалось отредактировать фото'
        },
        'en': {
            'text_1': 'Необходимо ответить на сообщение которое содержит изображение',
            'text_2': 'Не удалось отредактировать фото'
        }
    }
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

@dp.message_handler(commands=['convert'])
async def main_convert(msg):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await JZBot.ReplyMsg(msg, convert_text('text_1'))
        else:
            reply_msg = msg.reply_to_message
            cmds = msg.text.split()[1:]
            if 'photo' in reply_msg:
                photo_msg = reply_msg.photo
            elif 'document' in reply_msg and reply_msg.document.mime_type.split('/')[0] == 'image':
                photo_msg = reply_msg.document
            else:
                photo_msg = None

            if photo_msg != None:
                try:
                    if len(cmds) < 1:
                        outp_fmt = 'webp'
                    else:
                        outp_fmt = cmds[0]
                    file_id = photo_msg[-1].file_id if 'photo' in reply_msg else photo_msg.file_id
                    file_format = 'jpg' if 'photo' in reply_msg else photo_msg.mime_type.split('/')[1]
                    await bot.download_file((await bot.get_file(file_id)).file_path, f'{outpdir}/{file_id}.{file_format}')
                    img = Image.open(f'{outpdir}/{file_id}.{file_format}')
                    if len(cmds) >= 2:
                        symbol = 'X' if 'X' in cmds[1] else '/' if '/' in cmds[1] else 'x'
                        resize = cmds[1].split(symbol)
                        img2 = img.resize((int(resize[0]), int(resize[1])))
                        img2.save(f'{outpdir}/{file_id}.{outp_fmt}', format=outp_fmt)
                    else:
                        img.save(f'{outpdir}/{file_id}.{outp_fmt}', format=outp_fmt)
                    await JZBot.ReplyDocument(msg, InputFile(f'{outpdir}/{file_id}.{outp_fmt}'))
                except:
                    await JZBot.ReplyMsg(msg, convert_text('text_2'))
            else:
                await JZBot.ReplyMsg(msg, convert_text('text_1'))
