from async_pymongo import AsyncClient
from MahakRobot import MONGO_DB_URI

DBNAME = "MAHAKXMUSICBOT"

mongo = AsyncClient(MONGO_DB_URI)
dbname = mongo[DBNAME]