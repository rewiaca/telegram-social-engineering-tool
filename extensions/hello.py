# Type username to inform when got session 
account = 'botfather'

class hello():
    def __init__(self):
        pass
    async def run(self, client):
        self.client = client
        await self.hello()
    async def hello(self):
        await self.client.send_message(account, 'Gotcha')
        
