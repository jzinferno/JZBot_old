from JZBot import dp, GetChatStatus, GetBotLang, ReplyMsg, CreateBtn, AddBtns, ReplyMsg, EditBtns, RunShellCmd
from aiogram import types
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

sysInfoButtons = AddBtns(
    CreateBtn('Arch', 'arch'),
    CreateBtn('Hostname', 'hostname'),
    CreateBtn('Kernel', 'kernel'),
    CreateBtn('OS', 'os'),
    CreateBtn('Uptime', 'uptime'),
    CreateBtn('Host', 'host'),
    CreateBtn('Memory', 'memory'),
    CreateBtn('CPU', 'cpu'),
    CreateBtn('Uname', 'uname'),
    CreateBtn('Neofetch', 'neofetch')
)

sysInfoBack = AddBtns(
    CreateBtn(sysinfo_text('text_2'), 'back')
)

@dp.message_handler(commands=['sysinfo'])
async def main_sysinfo(msg: types.Message):
    if await GetChatStatus(msg) is not False:
        await ReplyMsg(msg, reply_markup=sysInfoButtons, text=sysinfo_text('text_1'))

@dp.callback_query_handler(lambda c: c.data in ['hostname', 'kernel', 'os', 'arch', 'uptime', 'host', 'memory', 'cpu', 'uname', 'neofetch', 'back'])
async def process_callback_button(cq: types.CallbackQuery):
    if cq.data == 'arch':
        await EditBtns(cq, reply_markup=sysInfoBack, text='Arch: ' + uname().machine)
    elif cq.data == 'hostname':
        await EditBtns(cq, reply_markup=sysInfoBack, text='Hostname: ' + uname().nodename)
    elif cq.data == 'kernel':
        await EditBtns(cq, reply_markup=sysInfoBack, text='Kernel: ' + uname().release)
    elif cq.data == 'os':
        await EditBtns(cq, reply_markup=sysInfoBack, text='OS: ' + (await RunShellCmd('neofetch distro', output=True)).split(': ')[-1])
    elif cq.data == 'uptime':
        await EditBtns(cq, reply_markup=sysInfoBack, text='Uptime: ' + (await RunShellCmd('neofetch uptime', output=True)).split(': ')[-1])
    elif cq.data == 'host':
        await EditBtns(cq, reply_markup=sysInfoBack, text='Host: ' + (await RunShellCmd('neofetch model', output=True)).split(': ')[-1])
    elif cq.data == 'memory':
        await EditBtns(cq, reply_markup=sysInfoBack, text='Memory: ' + (await RunShellCmd('neofetch memory', output=True)).split(': ')[-1])
    elif cq.data == 'cpu':
        await EditBtns(cq, reply_markup=sysInfoBack, text='CPU: ' + (await RunShellCmd('neofetch cpu', output=True)).split(': ')[-1])
    elif cq.data == 'uname':
        await EditBtns(cq, reply_markup=sysInfoBack, text=await RunShellCmd('uname -a', output=True))
    elif cq.data == 'neofetch':
        await EditBtns(cq, reply_markup=sysInfoBack, text='\n'.join([l for l in (await RunShellCmd('neofetch --stdout', output=True)).split('\n') if ':' in l]))
    else:
        await EditBtns(cq, reply_markup=sysInfoButtons, text=sysinfo_text('text_1'))
