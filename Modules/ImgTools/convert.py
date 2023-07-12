from JZBot import dp, bot, GetBotLang, GetChatStatus, outpdir, ReplyMsg, ReplyDocument, RundomName, DownloadFile, TextByLang, InputFile, Message
from PIL import Image

def convert_text(number):
    return TextByLang({
        'ru': [
            'Необходимо ответить на сообщение которое содержит изображение',
            'Не удалось отредактировать фото',
            'Максимально доступное разрешение 4K 4096x2160'
        ],
        'uk': [
            'Необхідно відповісти на повідомлення, яке містить зображення',
            'Не вдалося відредагувати фото',
            'Максимальна доступна роздільна здатність 4K 4096x2160'
        ],
        'en': [
            'Reply to a message that contains an image',
            'Failed to edit photo',
            'Maximum available resolution 4K 4096x2160'
        ]
    }, number)

@dp.message_handler(commands=['convert'])
async def main_convert(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, convert_text(0))
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
                    await DownloadFile(file_id, f'{outpdir}/{file_id}-{RandName}.{file_format}')
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
                            await ReplyMsg(msg, convert_text(2))
                except:
                    await ReplyMsg(msg, convert_text(1))
            else:
                await ReplyMsg(msg, convert_text(0))
