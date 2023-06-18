from JZBot import dp, GetChatStatus, GetBotLang, ReplyMsg, CreateBtn, AddBtns, ReplyMsg, EditBtns, RunShellCmd, TextByLang
from .memory import sysinfo_ram, sysinfo_swap, sysinfo_disk
from .distro import sysinfo_distro
from .uptime import sysinfo_uptime
from .cpu import sysinfo_cpu
from aiogram import types
from os import uname

def sysinfo_text(text):
    return TextByLang({
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
    }, text)

sysInfoButtons = AddBtns(
    CreateBtn('Arch', 'arch'),
    CreateBtn('Hostname', 'hostname'),
    CreateBtn('Kernel', 'kernel'),
    CreateBtn('OS', 'os'),
    CreateBtn('Uptime', 'uptime'),
    CreateBtn('Disk', 'disk'),
    CreateBtn('RAM', 'ram'),
    CreateBtn('Swap', 'swap'),
    CreateBtn('CPU', 'cpu'),
    CreateBtn('Uname', 'uname'),
    CreateBtn('Neofetch', 'neofetch')
)

def sysInfoBack(): 
    return AddBtns(CreateBtn(sysinfo_text('text_2'), 'back')
)

@dp.message_handler(commands=['sysinfo'])
async def main_sysinfo(msg: types.Message):
    if await GetChatStatus(msg) is not False:
        await ReplyMsg(msg, reply_markup=sysInfoButtons, text=sysinfo_text('text_1'))

@dp.callback_query_handler(lambda c: c.data in ['hostname', 'kernel', 'os', 'arch', 'uptime', 'disk', 'ram', 'swap', 'cpu', 'uname', 'neofetch', 'back'])
async def process_callback_button(cq: types.CallbackQuery):
    if cq.data == 'arch':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='Arch: ' + uname().machine)
    elif cq.data == 'hostname':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='Hostname: ' + uname().nodename)
    elif cq.data == 'kernel':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='Kernel: ' + uname().release)
    elif cq.data == 'os':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='OS: ' + sysinfo_distro())
    elif cq.data == 'uptime':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='Uptime: ' + sysinfo_uptime())
    elif cq.data == 'disk':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='Disk: ' + sysinfo_disk())
    elif cq.data == 'ram':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='RAM: ' + sysinfo_ram())
    elif cq.data == 'swap':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='Swap: ' + sysinfo_swap())
    elif cq.data == 'cpu':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='CPU: ' + sysinfo_cpu())
    elif cq.data == 'uname':
        await EditBtns(cq, reply_markup=sysInfoBack(), text=await RunShellCmd('uname -a', output=True))
    elif cq.data == 'neofetch':
        await EditBtns(cq, reply_markup=sysInfoBack(), text='\n'.join([l for l in (await RunShellCmd('neofetch --stdout', output=True)).split('\n') if ':' in l]))
    else:
        await EditBtns(cq, reply_markup=sysInfoButtons, text=sysinfo_text('text_1'))
