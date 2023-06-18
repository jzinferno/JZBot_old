def sysinfo_cpu():
    with open('/proc/cpuinfo', 'r') as f:
        inform = f.readlines()
    result = ''

    for line in inform:
        if line.startswith('model name'):
            result += ' '.join(line.split()[3:])
            break

    for line in inform:
        if line.startswith('Hardware'):
            if result != '':
                result += ' '
            result += ' '.join(line.split()[2:])
            break

    cores = 0
    for line in inform:
        if line.startswith('processor'):
            cores += 1
    result += f' ({cores})'

    with open(f'/sys/devices/system/cpu/cpu{cores - 1}/cpufreq/cpuinfo_max_freq', 'r') as f:
        result += f' @ {float(f.read().strip()) / 1000000}GHz'

    if '\n' in result:
        result = result.replace('\n', '')
    if ',' in result:
        result = result.replace(',', '')

    return result
