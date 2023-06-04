from main import dp, GetChatStatus, GetBotLang
from aiogram import types
from JZBot import JZBot
from os import uname

def sysinfo_text(text):
    full_text = {
        'ru': {
            'text_1': 'Выберите информацию о системе:',
            'text_2': 'Назад'
        },
        'uk': {
            'text_1': 'Виберіть інформацію про систему:',
            'text_2': 'Назад'
        },
        'en': {
            'text_1': 'Select system information:',
            'text_2': 'Back'
        }
    }
    if GetBotLang() in ['ru', 'uk']:
        result = full_text[GetBotLang()][text]
    else:
        result = full_text['en'][text]
    return result

sysInfoButtons = JZBot.AddBtns(
    JZBot.CreateBtn('Arch', 'arch'),
    JZBot.CreateBtn('Hostname', 'hostname'),
    JZBot.CreateBtn('Kernel', 'kernel'),
    JZBot.CreateBtn('OS', 'os'),
    JZBot.CreateBtn('Uptime', 'uptime'),
    JZBot.CreateBtn('Host', 'host'),
    JZBot.CreateBtn('Memory', 'memory'),
    JZBot.CreateBtn('CPU', 'cpu'),
    JZBot.CreateBtn('Uname', 'uname'),
    JZBot.CreateBtn('Neofetch', 'neofetch')
)

sysInfoBack = JZBot.AddBtns(
    JZBot.CreateBtn(sysinfo_text('text_2'), 'back')
)

@dp.message_handler(commands=['sysinfo'])
async def main_sysinfo(msg: types.Message):
    if await GetChatStatus(msg) is not False:
        await JZBot.ReplyMsg(msg, reply_markup=sysInfoButtons, text=sysinfo_text('text_1'))

@dp.callback_query_handler(lambda c: c.data in ['hostname', 'kernel', 'os', 'arch', 'uptime', 'host', 'memory', 'cpu', 'uname', 'neofetch', 'back'])
async def process_callback_button(cq: types.CallbackQuery):
    if cq.data == 'arch':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='Arch: ' + uname().machine)
    elif cq.data == 'hostname':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='Hostname: ' + uname().nodename)
    elif cq.data == 'kernel':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='Kernel: ' + uname().release)
    elif cq.data == 'os':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='OS: ' + (await JZBot.RunSysCmd('neofetch distro')).split(': ')[-1])
    elif cq.data == 'uptime':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='Uptime: ' + (await JZBot.RunSysCmd('neofetch uptime')).split(': ')[-1])
    elif cq.data == 'host':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='Host: ' + (await JZBot.RunSysCmd('neofetch model')).split(': ')[-1])
    elif cq.data == 'memory':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='Memory: ' + (await JZBot.RunSysCmd('neofetch memory')).split(': ')[-1])
    elif cq.data == 'cpu':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='CPU: ' + (await JZBot.RunSysCmd('neofetch cpu')).split(': ')[-1])
    elif cq.data == 'uname':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text=await JZBot.RunSysCmd('uname -a'))
    elif cq.data == 'neofetch':
        await JZBot.EditBtns(cq, reply_markup=sysInfoBack, text='\n'.join([l for l in (await JZBot.RunSysCmd('neofetch --stdout')).split('\n') if ':' in l]))
    else:
        await JZBot.EditBtns(cq, reply_markup=sysInfoButtons, text=sysinfo_text('text_1'))
