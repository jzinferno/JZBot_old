from JZBot import dp, ReplyMsg, RundomName, TextByLang

def genpasswd_text(text):
    return TextByLang({
        'ru': {
            'text_1': 'Введите количество символов для генерации пароля (максимум 250, по умолчанию 10)'
        },
        'uk': {
            'text_1': 'Введіть кількість символів для створення пароля (максимум 250, за замовчуванням 10)'
        },
        'en': {
            'text_1': 'Enter the number of characters to generate the password (max 250, default 10)'
        }
    }, text)

@dp.message_handler(commands=['genpasswd'])
async def main_genpasswd(msg):
    count = int(msg.text.split()[1]) if len(msg.text.split()) >= 2 else 10
    if count >= 251:
        await ReplyMsg(msg, genpasswd_text('text_1'))
    else:
        await ReplyMsg(msg, RundomName(count))
