import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient()

from config import config 
database = config.get('Main', 'database')
collection = config.get('Main', 'collection')

db = getattr(client, database)
collection = getattr(db, collection)
