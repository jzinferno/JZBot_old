from JZBot import dp, ReplyMsg, RundomName, TextByLang, Message

def genpasswd_text(number):
    return TextByLang({
        'ru': [
            'Введите количество символов для генерации пароля (максимум 250, по умолчанию 10)'
        ],
        'uk': [
            'Введіть кількість символів для створення пароля (максимум 250, за замовчуванням 10)'
        ],
        'en': [
            'Enter the number of characters to generate the password (max 250, default 10)'
        ]
    }, number)

@dp.message_handler(commands=['genpasswd'])
async def main_genpasswd(msg: Message):
    count = int(msg.text.split()[1]) if len(msg.text.split()) >= 2 else 10
    if count >= 251:
        await ReplyMsg(msg, genpasswd_text(0))
    else:
        await ReplyMsg(msg, RundomName(count))
