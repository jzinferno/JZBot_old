#!/usr/bin/env python3

from os.path import dirname, abspath, realpath
from os import chdir, environ, makedirs
from sys import platform

environ['JZBOT_WORKDIR'] = realpath(dirname(abspath(__file__)))

from JZBot import RunJZBot, outpdir, workdir
from Modules import dp

if __name__ == '__main__':
    makedirs(outpdir, exist_ok=True)
    chdir(workdir)
    if platform.startswith('linux'):
        RunJZBot()
    else:
        print('Only Linux is supported')
