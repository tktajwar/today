import re

def to_time(m):
    hour = m//60%24
    minute = m%60
    t = f"{hour:>2}:{minute:0>2}"
    return(t)

def to_min(duration):
    if(duration.isnumeric()):
        return(int(duration))
    if(':' in duration):
        s  = duration.split(':')
        return(int(s[0])*60 + int(s[1]))
    m = re.match("^(\d+)(\w)$", duration)
    if(not(m)):
        return(None)
    if(m.group(2)=='h'):
        return(int(m.group(1))*60)
    elif(m.group(2)=='d'):
        return(int(m.group(1))*60*24)
    elif(m.group(2)=='s'):
        return(int(m.group(1))/60)
    else:
        return(int(m.group(1)))

def is_duration(s):
    m = re.match("^(\d+)(\w)$", s)
    if(m):
        return(True)
    return(False)


