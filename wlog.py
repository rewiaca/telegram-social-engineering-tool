import datetime
from config import config 

log_file = config.get('Debug', 'log_file')
debug = config.getboolean('Debug','debug')

def wlog(message, date=True, display=True):
    message = str(message)
    if '\n' not in message[-2:]:
        message += '\n'
    if date:
        date = str(datetime.datetime.now())
        message = date + '\t' + message
    if display:
        print(message.rstrip())
    f = open(log_file, 'a')
    f.write(message)
    f.close()

if not debug:
    wlog = print 
