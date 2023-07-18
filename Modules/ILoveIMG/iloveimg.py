from JZBot import dp, outpdir, GetConfig, GetChatStatus, ReplyMsg, ReplyDocument, RundomName, DownloadFile, TextByLang, InputFile, Message
from .ILoveIMG import CompressIMG, ConvertIMG, CropIMG, ResizeIMG

iloveimg_key = GetConfig('iloveimg_key')

def iloveimg_text(number):
    return TextByLang({
        'ru': [
            'Необходимо ответить на сообщение которое содержит изображение',
            'Не удалось выполнить запрос на iloveimg.com',
            'Необходимо указать размер в пикселях'
        ],
        'uk': [
            'Необхідно відповісти на повідомлення, яке містить зображення',
            'Не вдалося виконати запит на iloveimg.com',
            'Необхідно вказати розмір в пікселях'
        ],
        'en': [
            'Reply to a message that contains an image',
            'Failed to complete request to iloveimg.com',
            'You must specify the size in pixels'
        ]
    }, number)

@dp.message_handler(commands=['compressimg'])
async def main_compressimg(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, iloveimg_text(0))
        else:
            reply_msg = msg.reply_to_message
            photo_msg = None
            if 'photo' in reply_msg:
                photo_msg = reply_msg.photo
            elif 'document' in reply_msg and reply_msg.document.mime_type.split('/')[0] == 'image':
                photo_msg = reply_msg.document

            if photo_msg != None:
                try:
                    file_id = photo_msg[-1].file_id if 'photo' in reply_msg else photo_msg.file_id
                    file_format = 'jpg' if 'photo' in reply_msg else photo_msg.mime_type.split('/')[1]
                    output_dir = outpdir + '/' + RundomName(15)
                    compression_level = 'recommended' if msg.text.find(' ') == -1  else msg.text.split()[1]
                    await DownloadFile(file_id, output_dir + '/input.' + file_format)
                    await CompressIMG(iloveimg_key).run(output_dir + '/input.' + file_format, output_dir + '/iloveimg.' + file_format, compression_level)
                    await ReplyDocument(msg, InputFile(output_dir + '/iloveimg.' + file_format))
                except:
                    await ReplyMsg(msg, iloveimg_text(1))
            else:
                await ReplyMsg(msg, iloveimg_text(0))

@dp.message_handler(commands=['convertimg'])
async def main_convertimg(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, iloveimg_text(0))
        else:
            reply_msg = msg.reply_to_message
            photo_msg = None
            if 'photo' in reply_msg:
                photo_msg = reply_msg.photo
            elif 'document' in reply_msg and reply_msg.document.mime_type.split('/')[0] == 'image':
                photo_msg = reply_msg.document

            if photo_msg != None:
                try:
                    file_id = photo_msg[-1].file_id if 'photo' in reply_msg else photo_msg.file_id
                    file_format = 'jpg' if 'photo' in reply_msg else photo_msg.mime_type.split('/')[1]
                    output_dir = outpdir + '/' + RundomName(15)
                    convert_format = 'webp' if msg.text.find(' ') == -1  else msg.text.split()[1]
                    await DownloadFile(file_id, output_dir + '/input.' + file_format)
                    await ConvertIMG(iloveimg_key).run(output_dir + '/input.' + file_format, output_dir + '/iloveimg.' + convert_format, convert_format)
                    await ReplyDocument(msg, InputFile(output_dir + '/iloveimg.' + convert_format))
                except:
                    await ReplyMsg(msg, iloveimg_text(1))
            else:
                await ReplyMsg(msg, iloveimg_text(0))

@dp.message_handler(commands=['cropimg'])
async def main_cropimg(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, iloveimg_text(0))
        else:
            reply_msg = msg.reply_to_message
            photo_msg = None
            if 'photo' in reply_msg:
                photo_msg = reply_msg.photo
            elif 'document' in reply_msg and reply_msg.document.mime_type.split('/')[0] == 'image':
                photo_msg = reply_msg.document

            if photo_msg != None:
                try:
                    if msg.text.find(' ') == -1:
                        await ReplyMsg(msg, iloveimg_text(2))
                    else:
                        text = msg.text.split()[1]
                        resize = text.split('X' if 'X' in text else '/' if '/' in text else 'x')
                        file_id = photo_msg[-1].file_id if 'photo' in reply_msg else photo_msg.file_id
                        file_format = 'jpg' if 'photo' in reply_msg else photo_msg.mime_type.split('/')[1]
                        output_dir = outpdir + '/' + RundomName(15)
                        await DownloadFile(file_id, output_dir + '/input.' + file_format)
                        await CropIMG(iloveimg_key).run(output_dir + '/input.' + file_format, output_dir + '/iloveimg.' + file_format, int(resize[0]), int(resize[1]))
                        await ReplyDocument(msg, InputFile(output_dir + '/iloveimg.' + file_format))
                except:
                    await ReplyMsg(msg, iloveimg_text(1))
            else:
                await ReplyMsg(msg, iloveimg_text(0))

@dp.message_handler(commands=['resizeimg'])
async def main_resizeimg(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, iloveimg_text(0))
        else:
            reply_msg = msg.reply_to_message
            photo_msg = None
            if 'photo' in reply_msg:
                photo_msg = reply_msg.photo
            elif 'document' in reply_msg and reply_msg.document.mime_type.split('/')[0] == 'image':
                photo_msg = reply_msg.document

            if photo_msg != None:
                try:
                    if msg.text.find(' ') == -1:
                        await ReplyMsg(msg, iloveimg_text(2))
                    else:
                        text = msg.text.split()[1]
                        resize = text.split('X' if 'X' in text else '/' if '/' in text else 'x')
                        file_id = photo_msg[-1].file_id if 'photo' in reply_msg else photo_msg.file_id
                        file_format = 'jpg' if 'photo' in reply_msg else photo_msg.mime_type.split('/')[1]
                        output_dir = outpdir + '/' + RundomName(15)
                        await DownloadFile(file_id, output_dir + '/input.' + file_format)
                        await ResizeIMG(iloveimg_key).run(output_dir + '/input.' + file_format, output_dir + '/iloveimg.' + file_format, int(resize[0]), int(resize[1]))
                        await ReplyDocument(msg, InputFile(output_dir + '/iloveimg.' + file_format))
                except:
                    await ReplyMsg(msg, iloveimg_text(1))
            else:
                await ReplyMsg(msg, iloveimg_text(0))
