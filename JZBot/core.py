from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, executor
import asyncio, json, os, random, string, sys
from pathlib import Path
from glob import glob
from os import getenv

workdir = getenv('JZBOT_WORKDIR')
configf = workdir + '/config.json'
outpdir = workdir + '/.out'

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

def SetConfig(key, value):
    with open(configf, 'r+') as jfile:
        data = json.load(jfile)
        data[key] = value
        jfile.seek(0)
        json.dump(data, jfile, indent=2)
        jfile.truncate()

def GetConfig(key):
    jfile = open(configf, 'r')
    result = json.load(jfile)
    jfile.close()
    if not key in result:
        SetConfig(key, '')
        return None
    return result[key]

def GetBotLang():
    return GetConfig('lang')

def TextByLang(full_text, text):
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

async def GetChatStatus(msg):
    jfile = open(configf, 'r')
    result = json.load(jfile)
    jfile.close()
    if str(msg.chat.id) in result['chats']:
        return True
    else:
        await ReplyMsg(msg, ':(')
    return False

bot = Bot(token=GetConfig('bot_token'))
dp = Dispatcher(bot)

async def DownloadFile(file_id, file_path):
    return await bot.download_file((await bot.get_file(file_id)).file_path, file_path)

def RunJZBot():
    executor.start_polling(dp, skip_updates=True)
