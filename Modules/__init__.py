from JZBot import workdir, GetBotLang
from os import path, listdir
import json

modulesdir = workdir + '/Modules'

def GetModules(full_path=False):
    ModulesArr = []
    for folder in listdir(modulesdir):
        folder_path = path.join(modulesdir, folder)
        if path.isdir(folder_path) and '__init__.py' in listdir(folder_path):
            ModulesArr.append(folder_path if full_path != False else folder)
    ModulesArr.sort()
    return ModulesArr

def GetModulesHelp():
    HelpArr = {}
    for ModuleDir in GetModules(full_path=True):
        with open(ModuleDir + '/module.json', 'r+') as jfile:
            data = json.load(jfile)
        HelpArr[ModuleDir.split('/')[-1]] = {'author': data['author'], 'help': data['help'][GetBotLang()]}
    return HelpArr

for ModuleDir in GetModules():
    exec('from Modules.{} import dp'.format(ModuleDir))
