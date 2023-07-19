from JZBot import dp, outpdir, GetConfig, GetChatStatus, ReplyMsg, ReplyDocument, RundomName, DownloadFile, TextByLang, InputFile, Message
from .ILovePDF import CompressPDF, ImagePDF, OfficePDF, ProtectPDF, UnlockPDF

ilovepdf_key = GetConfig('ilovepdf_key')

def ilovepdf_text(number):
    return TextByLang({
        'ru': [
            'Необходимо ответить на сообщение которое содержит изображение',
            'Необходимо ответить на сообщение которое содержит PDF файл',
            'Необходимо ответить на сообщение которое содержит оффисный файл',
            'Необходимо указать пароль',
            'Не удалось выполнить запрос на ilovepdf.com'
        ],
        'uk': [
            'Необхідно відповісти на повідомлення, що містить зображення',
            'Необхідно відповісти на повідомлення, що містить файл PDF',
            'Необхідно відповісти на повідомлення, що містить офісний файл',
            'Необхідно вказати пароль',
            'Не вдалося виконати запит на ilovepdf.com'
        ],
        'en': [
            'Need to reply to a message that contains an image',
            'Need to reply to a message that contains a PDF file',
            'Need to reply to a message that contains an office file',
            'Need to provide a password',
            'Failed to execute the request to ilovepdf.com'
        ]
    }, number)

@dp.message_handler(commands=['compresspdf'])
async def main_compresspdf(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, ilovepdf_text(1))
        else:
            reply_msg = msg.reply_to_message
            pdf_msg = reply_msg.document if 'document' in reply_msg and reply_msg.document.mime_type.split('/')[-1] == 'pdf' else None

            if pdf_msg != None:
                try:
                    output_dir = outpdir + '/' + RundomName(15)
                    compression_level = 'recommended' if msg.text.find(' ') == -1  else msg.text.split()[1]
                    await DownloadFile(pdf_msg.file_id, output_dir + '/input.pdf')
                    await CompressPDF(ilovepdf_key).run(output_dir + '/input.pdf', output_dir + '/ilovepdf.pdf', compression_level)
                    await ReplyDocument(msg, InputFile(output_dir + '/ilovepdf.pdf'))
                except:
                    await ReplyMsg(msg, ilovepdf_text(4))
            else:
                await ReplyMsg(msg, ilovepdf_text(1))

@dp.message_handler(commands=['imagepdf'])
async def main_imagepdf(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, ilovepdf_text(0))
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
                    await DownloadFile(file_id, output_dir + '/input.' + file_format)
                    await ImagePDF(ilovepdf_key).run(output_dir + '/input.' + file_format, output_dir + '/ilovepdf.pdf')
                    await ReplyDocument(msg, InputFile(output_dir + '/ilovepdf.pdf'))
                except:
                    await ReplyMsg(msg, ilovepdf_text(4))
            else:
                await ReplyMsg(msg, ilovepdf_text(0))

@dp.message_handler(commands=['officepdf'])
async def main_officepdf(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, ilovepdf_text(2))
        else:
            reply_msg = msg.reply_to_message
            office_formats = ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'odt', 'odp', 'ods']
            office_msg = reply_msg.document if 'document' in reply_msg and reply_msg.document.file_name.split('.')[-1] in office_formats else None

            if office_msg != None:
                try:
                    file_format = office_msg.file_name.split('.')[-1]
                    output_dir = outpdir + '/' + RundomName(15)
                    await DownloadFile(office_msg.file_id, output_dir + '/input.' + file_format)
                    await OfficePDF(ilovepdf_key).run(output_dir + '/input.' + file_format, output_dir + '/ilovepdf.pdf')
                    await ReplyDocument(msg, InputFile(output_dir + '/ilovepdf.pdf'))
                except:
                    await ReplyMsg(msg, ilovepdf_text(4))
            else:
                await ReplyMsg(msg, ilovepdf_text(2))

@dp.message_handler(commands=['protectpdf'])
async def main_protectpdf(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, ilovepdf_text(1))
        else:
            reply_msg = msg.reply_to_message
            pdf_msg = reply_msg.document if 'document' in reply_msg and reply_msg.document.mime_type.split('/')[-1] == 'pdf' else None

            if pdf_msg != None:
                try:
                    output_dir = outpdir + '/' + RundomName(15)
                    if msg.text.find(' ') == -1:
                        await ReplyMsg(msg, ilovepdf_text(3))
                    else:
                        await DownloadFile(pdf_msg.file_id, output_dir + '/input.pdf')
                        await ProtectPDF(ilovepdf_key).run(output_dir + '/input.pdf', output_dir + '/ilovepdf.pdf', msg.text.split()[1])
                        await ReplyDocument(msg, InputFile(output_dir + '/ilovepdf.pdf'))
                except:
                    await ReplyMsg(msg, ilovepdf_text(4))
            else:
                await ReplyMsg(msg, ilovepdf_text(1))

@dp.message_handler(commands=['unlockpdf'])
async def main_unlockpdf(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, ilovepdf_text(1))
        else:
            reply_msg = msg.reply_to_message
            pdf_msg = reply_msg.document if 'document' in reply_msg and reply_msg.document.mime_type.split('/')[-1] == 'pdf' else None

            if pdf_msg != None:
                try:
                    output_dir = outpdir + '/' + RundomName(15)
                    await DownloadFile(pdf_msg.file_id, output_dir + '/input.pdf')
                    await UnlockPDF(ilovepdf_key).run(output_dir + '/input.pdf', output_dir + '/ilovepdf.pdf')
                    await ReplyDocument(msg, InputFile(output_dir + '/ilovepdf.pdf'))
                except:
                    await ReplyMsg(msg, ilovepdf_text(4))
            else:
                await ReplyMsg(msg, ilovepdf_text(1))
