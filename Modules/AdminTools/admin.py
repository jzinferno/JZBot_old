from JZBot import dp, GetBotLang, GetChatStatus, SetConfig, CreateBtn, AddBtns, ReplyMsg, EditBtns, TextByLang, CallbackQuery, Message

def admin_text(number):
    return TextByLang({
        'ru': [
            'Выберите язык или ввойдите',
            'Выберите язык, сейчас выбран: ',
            'Язык бота',
            'Настройки',
            'Назад'
        ],
        'uk': [
            'Виберіть мову або увійдіть',
            'Виберіть мову, зараз вибраний: ',
            'Мова бота',
            'Налаштування',
            'Назад'
        ],
        'en': [
            'Choose a language or sign in',
            'Select language, currently selected: ',
            'Bot language',
            'Settings',
            'Back'
        ]
    }, number)

def settingsBtns():
    return AddBtns(
        CreateBtn(admin_text(2), 'set_lang'),
        CreateBtn(admin_text(3), 'sign_in')
    )

def langsBtns():
    return AddBtns(
        CreateBtn('Ru', 'ru_lang'),
        CreateBtn('Uk', 'uk_lang'),
        CreateBtn('En', 'en_lang'),
        CreateBtn(admin_text(4), 'lang_back_btn'),
    )

@dp.message_handler(commands=['admin'])
async def main_admin(msg: Message):
    if await GetChatStatus(msg) is not False:
        await ReplyMsg(msg, text=admin_text(0), reply_markup=settingsBtns())

@dp.callback_query_handler(lambda c: c.data in ['set_lang', 'sign_in', 'ru_lang', 'uk_lang', 'en_lang', 'lang_back_btn'])
async def process_callback_button(cq: CallbackQuery):
    if cq.data == 'set_lang':
        await EditBtns(cq, text=admin_text(1) + GetBotLang(), reply_markup=langsBtns())
    elif cq.data == 'ru_lang':
        SetConfig('lang', 'ru')
        await EditBtns(cq, text=admin_text(1) + GetBotLang(), reply_markup=langsBtns())
    elif cq.data == 'uk_lang':
        SetConfig('lang', 'uk')
        await EditBtns(cq, text=admin_text(1) + GetBotLang(), reply_markup=langsBtns())
    elif cq.data == 'en_lang':
        SetConfig('lang', 'en')
        await EditBtns(cq, text=admin_text(1) + GetBotLang(), reply_markup=langsBtns())
    elif cq.data == 'lang_back_btn':
        await EditBtns(cq, text=admin_text(0), reply_markup=settingsBtns())
    else:
        await EditBtns(cq, text='No No No')
