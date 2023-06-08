from JZBot import dp, bot, GetBotLang, GetChatStatus, outpdir, ReplyMsg, ReplyDocument, RundomName
from aiogram.types import InputFile
from PIL import Image

def convert_text(text):
    full_text = {
        'ru': {
            'text_1': 'Необходимо ответить на сообщение которое содержит изображение',
            'text_2': 'Не удалось отредактировать фото',
            'text_3': 'Максимально доступное разрешение 4K 4096x2160'
        },
        'uk': {
            'text_1': 'Необхідно відповісти на повідомлення, яке містить зображення',
            'text_2': 'Не вдалося відредагувати фото',
            'text_3': 'Максимальна доступна роздільна здатність 4K 4096x2160'
        },
        'en': {
            'text_1': 'Reply to a message that contains an image',
            'text_2': 'Failed to edit photo',
            'text_3': 'Maximum available resolution 4K 4096x2160'
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
            await ReplyMsg(msg, convert_text('text_1'))
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
                    RandName = RundomName(5)
                    await bot.download_file((await bot.get_file(file_id)).file_path, f'{outpdir}/{file_id}-{RandName}.{file_format}')
                    img = Image.open(f'{outpdir}/{file_id}-{RandName}.{file_format}')
                    if len(cmds) < 2:
                        img.save(f'{outpdir}/{file_id}-{RandName}.{outp_fmt}', format=outp_fmt)
                        await ReplyDocument(msg, InputFile(f'{outpdir}/{file_id}-{RandName}.{outp_fmt}'))
                    else:
                        symbol = 'X' if 'X' in cmds[1] else '/' if '/' in cmds[1] else 'x'
                        resize = cmds[1].split(symbol)
                        if int(resize[0]) <= 4096 and int(resize[1]) <= 2160:
                            img2 = img.resize((int(resize[0]), int(resize[1])))
                            img2.save(f'{outpdir}/{file_id}-{RandName}.{outp_fmt}', format=outp_fmt)
                            await ReplyDocument(msg, InputFile(f'{outpdir}/{file_id}-{RandName}.{outp_fmt}'))
                        else:
                            await ReplyMsg(msg, convert_text('text_3'))
                except:
                    await ReplyMsg(msg, convert_text('text_2'))
            else:
                await ReplyMsg(msg, convert_text('text_1'))
