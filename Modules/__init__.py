from JZBot import workdir
from glob import glob
from os import path

for ModuleDir in [d for d in glob(workdir + '/Modules/*') if path.isfile(path.join(d, '__init__.py'))]:
    exec('from Modules.{} import dp'.format(ModuleDir.split('/')[-1]))
