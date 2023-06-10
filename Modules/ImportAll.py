from JZBot import workdir
from os.path import realpath, dirname
from os import walk

for ModuleDir in [root for root, dirs, files in walk(f'{workdir}/Modules') if 'module.py' in files]:
    exec('from Modules.{}.module import dp'.format(ModuleDir.split('/')[-1]))
