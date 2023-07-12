from JZBot import dp, version, GetChatStatus, ReplyMsg, Message

@dp.message_handler(commands=['id'])
async def main_id(msg: Message):
    await ReplyMsg(msg, msg.chat.id)

@dp.message_handler(commands=['myid'])
async def main_myid(msg: Message):
    await ReplyMsg(msg, msg.from_user.id)

@dp.message_handler(commands=['version'])
async def main_version(msg: Message):
    await ReplyMsg(msg, version)
