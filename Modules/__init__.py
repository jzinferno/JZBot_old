from JZBot import workdir
from os.path import realpath, dirname
from os import path, walk
from glob import glob

for ModuleDir in [d for d in glob(workdir + '/Modules/*') if path.isfile(path.join(d, '__init__.py'))]:
    exec('from Modules.{} import dp'.format(ModuleDir.split('/')[-1]))
