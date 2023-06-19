from JZBot import dp, version, GetChatStatus, ReplyMsg

@dp.message_handler(commands=['id'])
async def main_id(msg):
    await ReplyMsg(msg, msg.chat.id)

@dp.message_handler(commands=['myid'])
async def main_myid(msg):
    await ReplyMsg(msg, msg.from_user.id)

@dp.message_handler(commands=['version'])
async def main_version(msg):
    await ReplyMsg(msg, version)
