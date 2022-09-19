import re

# format minutes to H:m
def to_time(m):
    hour = m//60%24
    minute = m%60
    t = f"{hour:>2}:{minute:0>2}"
    return(t)

# turn string to minutes
def to_min(duration):
    # INT (minutes)
    if(duration.isnumeric()):
        return(int(duration))

    # hour:minutes format
    if(':' in duration):
        s  = duration.split(':')
        return(int(s[0])*60 + int(s[1]))

    # 3h / 30m / etc.
    m = re.match("^(\d+)(\w)$", duration)
    if(not(m)):
        return(None)
    elif(m.group(2)=='d'): # days
        return(int(m.group(1))*60*24)
    if(m.group(2)=='h'): # hours
        return(int(m.group(1))*60)
    elif(m.group(2)=='s'): # seconds
        return(int(m.group(1))/60)
    else: # minutes
        return(int(m.group(1)))

# check if string is duration
def is_duration(s):
    # hour:minute
    if(':' in s):
        return(True)

    # 3h / 30m / etc.
    m = re.match("^(\d+)(\w)$", s)
    if(m):
        return(True)

    return(False)
