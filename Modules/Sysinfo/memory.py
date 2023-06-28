import shutil

def getMemInfoValue(string):
    with open('/proc/meminfo', 'r') as f:
        result = 0
        for line in f.readlines():
            if line.startswith(string):
                result = int(line.split()[1]) // 1024
                break
    return result

def sysinfo_ram():
    total = getMemInfoValue('MemTotal')
    used = total - getMemInfoValue('MemAvailable')
    return f'{used}MiB / {total}MiB ({int(used / total * 100)})%'

def sysinfo_swap():
    total = getMemInfoValue('SwapTotal')
    used = total - getMemInfoValue('SwapFree')
    return f'{used}MiB / {total}MiB ({int(used / total * 100)})%'

def sysinfo_disk():
    total, used, free = shutil.disk_usage('.')
    return f'{used // 1073741824}GiB / {total // 1073741824}GiB ({int(used / total * 100)}%)'
