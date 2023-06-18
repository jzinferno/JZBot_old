from JZBot import RunShellCmd
from os.path import exists

def sysinfo_distro():
    if exists('/system/build.prop'):
        distro_name = 'Android ' + RunShellCmd('getprop ro.build.version.release', output=True)
    elif exists('/etc/os-release'):
        with open('/etc/os-release') as f:
            for line in f:
                if line.startswith('NAME='):
                    distro_name = line.split('=')[1].strip().strip('\"')
    else:
        distro_name = 'Unknown'
    return distro_name
