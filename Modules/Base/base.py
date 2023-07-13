from JZBot import dp, version, GetChatStatus, GetBotLang, ReplyMsg, Message
from Modules import GetModulesHelp

@dp.message_handler(commands=['help', 'start'])
async def main_version(msg: Message):
    JZBotHelpFull = GetModulesHelp()
    if len(msg.text.split()[1:]) >= 1:
        ModuleName = msg.text.split()[1]
        if ModuleName in JZBotHelpFull:
            await ReplyMsg(msg, JZBotHelpFull[ModuleName]['help'])
        else:
            await ReplyMsg(msg, 'No module: ' + ModuleName)
    else:
        JZBotHelp = ['https://github.com/jzinferno/JZBot\n', '/help <module name>\n', 'Installed Modules:']
        for ModuleName in JZBotHelpFull:
            JZBotHelp.append(ModuleName + ' - ' + JZBotHelpFull[ModuleName]['author'])
        await ReplyMsg(msg, '\n'.join(JZBotHelp))

@dp.message_handler(commands=['id'])
async def main_id(msg: Message):
    await ReplyMsg(msg, msg.chat.id)

@dp.message_handler(commands=['userid'])
async def main_userid(msg: Message):
    id = msg.reply_to_message.from_user.id if 'reply_to_message' in msg else msg.from_user.id
    await ReplyMsg(msg, id)

@dp.message_handler(commands=['version'])
async def main_version(msg: Message):
    await ReplyMsg(msg, version)
