def getMemInfoValue(string):
    with open('/proc/meminfo', 'r') as f:
        result = 0
        for line in f.readlines():
            if line.startswith(string):
                result = int(line.split()[1]) // 1024
                break
    return result

def sysinfo_ram():
    return str(getMemInfoValue('MemTotal') - getMemInfoValue('MemAvailable')) + 'MiB / ' + str(getMemInfoValue('MemTotal')) + 'MiB'

def sysinfo_swap():
    return str(getMemInfoValue('SwapTotal') - getMemInfoValue('SwapFree')) + 'MiB / ' + str(getMemInfoValue('SwapTotal')) + 'MiB'
