from os.path import exists
import subprocess

def sysinfo_distro():
    if exists('/system') and exists('/vendor') and exists('/data'):
        distro_name = 'Android ' + subprocess.run(['getprop', 'ro.build.version.release'], capture_output=True).stdout.decode('utf-8')
    elif exists('/etc/os-release'):
        with open('/etc/os-release') as f:
            for line in f:
                if line.startswith('NAME='):
                    distro_name = line.split('=')[1].strip().strip('\"')
    else:
        distro_name = 'Unknown'
    return distro_name
