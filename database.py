from mongoengine.connection import connect
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = (
    "mongodb://root:example@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false",
)

client = AsyncIOMotorClient(MONGODB_URL)
db = client.its_about_time
