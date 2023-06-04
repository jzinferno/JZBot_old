#!/usr/bin/env python3

from JZBot import RunJZBot, workdir
from os import chdir

if __name__ == '__main__':
    chdir(workdir)
    RunJZBot()
