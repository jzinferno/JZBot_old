from main import dp, AddChatToList, GetChatStatus, database
from JZBot import JZBot

@dp.message_handler(commands=['id'])
async def main_id(msg):
    AddChatToList(msg.chat.id)
    await JZBot.ReplyMsg(msg, msg.chat.id)

@dp.message_handler(commands=['myid'])
async def main_myid(msg):
    AddChatToList(msg.chat.id)
    await JZBot.ReplyMsg(msg, msg.from_user.id)

@dp.message_handler(commands=['chats'])
async def main_chats(msg):
    if await GetChatStatus(msg) is not False:
        await JZBot.ReplyMsg(msg, JZBot.SqlFetchOne(database, 'SELECT COUNT(ChatId) FROM ChatList')[0])