from os.path import dirname, abspath, realpath
from .core import ReplyMsg
import json

workdir = realpath(dirname(abspath(__file__)) + '/..')
configf = workdir + '/config.json'
outpdir = workdir + '/.out'

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
