#!/usr/bin/env python3

from os.path import dirname, abspath, realpath
from os import chdir, environ, makedirs

environ['JZBOT_WORKDIR'] = realpath(dirname(abspath(__file__)))

from JZBot import RunJZBot, outpdir, workdir
from Modules.ImportAll import dp

if __name__ == '__main__':
    makedirs(outpdir, exist_ok=True)
    chdir(workdir)
    RunJZBot()
