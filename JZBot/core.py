from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio, sqlite3, random, string

async def SendMsg(msg, *args1, **args2):
    try:
        await msg.answer(*args1, **args2)
    except:
        print('JZBot: error send message')

async def SendAudio(msg, *args1, **args2):
    try:
        await msg.answer_audio(*args1, **args2)
    except:
        print('JZBot: error send audio')

async def SendDocument(msg, *args1, **args2):
    try:
        await msg.answer_document(*args1, **args2)
    except:
        print('JZBot: error send document')

async def SendPhoto(msg, *args1, **args2):
    try:
        await msg.answer_photo(*args1, **args2)
    except:
        print('JZBot: error send photo')

async def SendVoice(msg, *args1, **args2):
    try:
        await msg.answer_voice(*args1, **args2)
    except:
        print('JZBot: error send voice')

async def ReplyMsg(msg, *args1, **args2):
    try:
        await msg.reply(*args1, **args2)
    except:
        await SendMsg(msg, *args1, **args2)

async def ReplyAudio(msg, *args1, **args2):
    try:
        await msg.reply_audio(*args1, **args2)
    except:
        await SendAudio(msg, *args1, **args2)

async def ReplyDocument(msg, *args1, **args2):
    try:
        await msg.reply_document(*args1, **args2)
    except:
        await SendDocument(msg, *args1, **args2)

async def ReplyPhoto(msg, *args1, **args2):
    try:
        await msg.reply_photo(*args1, **args2)
    except:
        await SendPhoto(msg, *args1, **args2)
    
async def ReplyVoice(msg, *args1, **args2):
    try:
        await msg.reply_voice(*args1, **args2)
    except:
        await SendVoice(msg, *args1, **args2)

def CreateBtn(text, data):
    return InlineKeyboardButton(text, callback_data=data)

def AddBtns(*args):
    return InlineKeyboardMarkup(row_width=2).add(*args)

async def EditBtns(cq, **args):
    try:
        await cq.message.edit_text(**args)
    except:
        pass

def RundomName(count):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(count)])

async def RunShellCmd(command, output=False, error=False):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    if not output and not error:
        await process.communicate()
        return

    stdout, stderr = await process.communicate()

    if output and error:
        return stdout.decode().strip(), stderr.decode().strip()
    elif output:
        return stdout.decode().strip()
    else:
        return stderr.decode().strip()
