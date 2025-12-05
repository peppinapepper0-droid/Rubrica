from pymongo import AsyncMongoClient

MONGO_URL = "rubricas://localhost:27017"
DB_NAME = "rubrica"
COOKIE_SECRET = "super_secret_key_change_me"
PORT = 8888

client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

users = db["users"]
messaggi = db["messaggi"]
