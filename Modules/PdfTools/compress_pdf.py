from JZBot import dp, GetChatStatus, outpdir, ReplyMsg, ReplyDocument, RundomName, DownloadFile, TextByLang, RunShellCmd, InputFile, Message

def compress_pdf_text(number):
    return TextByLang({
        'ru': [
            'Необходимо ответить на сообщение которое содержит pdf файл',
            'Не удалось сжать pdf'
        ],
        'uk': [
            'Необхідно відповісти на повідомлення, яке містить pdf файл',
            'Не вдалося стиснути pdf'
        ],
        'en': [
            'Reply to a message that contains a pdf file',
            'Failed to compress pdf'
        ]
    }, number)

async def compress_pdf(input_file, output_file):
    await RunShellCmd(f'gs -q -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile={output_file} {input_file}')

@dp.message_handler(commands=['compress'])
async def main_compress(msg: Message):
    if await GetChatStatus(msg) is not False:
        if 'reply_to_message' not in msg:
            await ReplyMsg(msg, compress_pdf_text(0))
        else:
            reply_msg = msg.reply_to_message
            if reply_msg.document.mime_type.split('/')[-1] == 'pdf':
                try:
                    file_id = reply_msg.document.file_id
                    FileName = f'{outpdir}/{file_id}-{RundomName(10)}'
                    await DownloadFile(file_id, FileName + '.pdf')
                    await compress_pdf(FileName + '.pdf', FileName + '-compressed.pdf')
                    await ReplyDocument(msg, InputFile(FileName + '-compressed.pdf'))
                except:
                    await ReplyMsg(msg, compress_pdf_text(1))
            else:
                await ReplyMsg(msg, compress_pdf_text(0))
        
