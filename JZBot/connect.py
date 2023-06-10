from .config import GetConfig, outpdir, workdir, configf
from aiogram import Bot, Dispatcher, executor
from pathlib import Path
from glob import glob
import sys, os

bot = Bot(token=GetConfig('bot_token'))
dp = Dispatcher(bot)

async def DownloadFile(file_id, file_path):
    return await bot.download_file((await bot.get_file(file_id)).file_path, file_path)

def RunJZBot():
    os.makedirs(outpdir, exist_ok=True)
    sys.path.append(workdir + '/Modules')
    for file in glob(os.path.join(workdir, 'Modules/*.py')):
        module = file.split('/')[-1].split('.')[0]
        exec('from Modules.{} import dp'.format(module))
    executor.start_polling(dp)
