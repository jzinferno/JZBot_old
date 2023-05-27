from main import dp, workdir, GetBotLang, GetChatStatus, SetConfig
from aiogram import types
from JZBot import JZBot

def admin_text(text):
    full_text = {
        'ru': {
            'text_1': 'Выберите язык или ввойдите',
            'text_2': 'Выберите язык, сейчас выбран: ',
            'text_3': 'Язык бота',
            'text_4': 'Настройки'
        },
        'uk': {
            'text_1': 'Виберіть мову або увійдіть',
            'text_2': 'Виберіть мову, зараз вибраний: ',
            'text_3': 'Мова бота',
            'text_4': 'Налаштування'
        },
        'en': {
            'text_1': 'Choose a language or sign in',
            'text_2': 'Select language, currently selected: ',
            'text_3': 'Bot language',
            'text_4': 'Settings'
        }
    }
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

def settingsBtns():
    return JZBot.AddBtns(
        JZBot.CreateBtn(admin_text('text_3'), 'set_lang'),
        JZBot.CreateBtn(admin_text('text_4'), 'sign_in')
    )

langsBtns = JZBot.AddBtns(
    JZBot.CreateBtn('Ru', 'ru_lang'),
    JZBot.CreateBtn('Uk', 'uk_lang'),
    JZBot.CreateBtn('En', 'en_lang'),
    JZBot.CreateBtn('Back', 'lang_back_btn'),
)

@dp.message_handler(commands=['admin'])
async def main_admin(msg: types.Message):
    if await GetChatStatus(msg) is not False:
        await JZBot.ReplyMsg(msg, text=admin_text('text_1'), reply_markup=settingsBtns())

@dp.callback_query_handler(lambda c: c.data in ['set_lang', 'sign_in', 'ru_lang', 'uk_lang', 'en_lang', 'lang_back_btn'])
async def process_callback_button(cq: types.CallbackQuery):
    if cq.data == 'set_lang':
        await JZBot.EditBtns(cq, text=admin_text('text_2') + GetBotLang(), reply_markup=langsBtns)
    elif cq.data == 'ru_lang':
        SetConfig('lang', 'ru')
        await JZBot.EditBtns(cq, text=admin_text('text_2') + GetBotLang(), reply_markup=langsBtns)
    elif cq.data == 'uk_lang':
        SetConfig('lang', 'uk')
        await JZBot.EditBtns(cq, text=admin_text('text_2') + GetBotLang(), reply_markup=langsBtns)
    elif cq.data == 'en_lang':
        SetConfig('lang', 'en')
        await JZBot.EditBtns(cq, text=admin_text('text_2') + GetBotLang(), reply_markup=langsBtns)
    elif cq.data == 'lang_back_btn':
        await JZBot.EditBtns(cq, text=admin_text('text_1'), reply_markup=settingsBtns())
    else:
        await JZBot.EditBtns(cq, text='No No No')
