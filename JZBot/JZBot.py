from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio, sqlite3, random, string

class _JZBot():
    async def SendMsg(self, msg, *args1, **args2):
        try:
            await msg.answer(*args1, **args2)
        except:
            print('JZBot: error send message')

    async def SendAudio(self, msg, *args1, **args2):
        try:
            await msg.answer_audio(*args1, **args2)
        except:
            print('JZBot: error send audio')

    async def SendDocument(self, msg, *args1, **args2):
        try:
            await msg.answer_document(*args1, **args2)
        except:
            print('JZBot: error send document')

    async def SendPhoto(self, msg, *args1, **args2):
        try:
            await msg.answer_photo(*args1, **args2)
        except:
            print('JZBot: error send photo')

    async def SendVoice(self, msg, *args1, **args2):
        try:
            await msg.answer_voice(*args1, **args2)
        except:
            print('JZBot: error send voice')

    async def ReplyMsg(self, msg, *args1, **args2):
        try:
            await msg.reply(*args1, **args2)
        except:
            await SendMsg(msg, *args1, **args2)

    async def ReplyAudio(self, msg, *args1, **args2):
        try:
            await msg.reply_audio(*args1, **args2)
        except:
            await SendAudio(msg, *args1, **args2)

    async def ReplyDocument(self, msg, *args1, **args2):
        try:
            await msg.reply_document(*args1, **args2)
        except:
            await SendDocument(msg, *args1, **args2)

    async def ReplyPhoto(self, msg, *args1, **args2):
        try:
            await msg.reply_photo(*args1, **args2)
        except:
            await SendPhoto(msg, *args1, **args2)
    
    async def ReplyVoice(self, msg, *args1, **args2):
        try:
            await msg.reply_voice(*args1, **args2)
        except:
            await SendVoice(msg, *args1, **args2)

    def CreateBtn(self, text, data):
        return InlineKeyboardButton(text, callback_data=data)

    def AddBtns(self, *args):
        return InlineKeyboardMarkup(row_width=2).add(*args)

    async def EditBtns(self, cq, **args):
        try:
            await cq.message.edit_text(**args)
        except:
            pass

    def SqlCommit(self, sql_db, sdl_cmd):
        connect = sqlite3.connect(sql_db)
        cursor = connect.cursor()
        try:
            cursor.execute(sdl_cmd)
            connect.commit()
        except:
            print('Syntax error!')
        connect.close()

    def SqlFetchAll(self, sql_db, sdl_cmd):
        connect = sqlite3.connect(sql_db)
        cursor = connect.cursor()
        try:
            cursor.execute(sdl_cmd)
            result = cursor.fetchall()
        except:
            print('Syntax error!')
        connect.close()
        return result

    def SqlFetchOne(self, sql_db, sdl_cmd):
        connect = sqlite3.connect(sql_db)
        cursor = connect.cursor()
        try:
            cursor.execute(sdl_cmd)
            result = cursor.fetchone()
        except:
            print('Syntax error!')
        connect.close()
        return result
    
    def RundomName(self, count):
        return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(count)])

    async def RunSysCmd(self, command):
        process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        return stdout.decode().strip()

JZBot = _JZBot()