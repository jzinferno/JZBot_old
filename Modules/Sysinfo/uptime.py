from uptime import uptime

def sysinfo_uptime():
    seconds = uptime()

    minute = 60
    hour = 3600
    day = 86400
    month = 2592000
    year = 31536000
    
    years = seconds // year
    seconds %= year
    months = seconds // month
    seconds %= month
    days = seconds // day
    seconds %= day
    hours = seconds // hour
    seconds %= hour
    minutes = seconds // minute
    seconds %= minute
    
    result = ''
    if years > 0:
        result += str(int(years)) + ' years, '
    if months > 0:
        result += str(int(months)) + ' months, '
    if days > 0:
        result += str(int(days)) + ' days, '
    if hours > 0:
        result += str(int(hours)) + ' hours, '
    if minutes > 0:
        result += str(int(minutes)) + ' mins'
        
    return result.strip(', ')