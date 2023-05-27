#!/usr/bin/env python3

from aiogram import Bot, Dispatcher, executor
from os.path import dirname, abspath
from JZBot import JZBot
from glob import glob
from os import chdir
import sys, os, json

workdir = dirname(abspath(__file__))
database = workdir + '/database.db'
configf = workdir + '/config.json'
outpdir = workdir + '/.out'

def SetConfig(key: str, value: str):
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

def main_text(text):
    full_text = {
        'ru': {
            'text_1': 'Id этого чат не был добавлен в список чатов бота'
        },
        'uk': {
            'text_1': 'Id цього чату не було додано до списку чатів бота'
        },
        'en': {
            'text_1': 'This chat ID has not been added to the bot\'s chat list'
        }
    }
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

def AddChatToList(ChatId):
    JZBot.SqlCommit(database, 'INSERT INTO ChatList (ChatId, Status) SELECT {}, {} WHERE NOT EXISTS (SELECT * FROM ChatList WHERE ChatId = {})'.format(ChatId, False, ChatId))

async def GetChatStatus(msg):
    AddChatToList(msg.chat.id)
    result = JZBot.SqlFetchOne(database, 'SELECT * FROM ChatList WHERE ChatId = {} AND Status = {}'.format(msg.chat.id, True)) is not None
    if result == False:
        await JZBot.ReplyMsg(msg, main_text('text_1'))
    return result

bot = Bot(token=GetConfig('bot_token'))
dp = Dispatcher(bot)

if __name__ == '__main__':
    chdir(workdir)
    os.makedirs(outpdir, exist_ok=True)
    sys.path.append(workdir + '/modules')
    JZBot.SqlCommit(database, 'CREATE TABLE IF NOT EXISTS ChatList (Id INTEGER PRIMARY KEY AUTOINCREMENT, ChatId INTEGER, Status BOOLEAN)')
    for file in glob(os.path.join(workdir, 'modules/*.py')):
        module = file.split('/')[-1].split('.')[0]
        exec('from modules.{} import dp'.format(module))
    executor.start_polling(dp)
