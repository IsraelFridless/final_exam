from pymongo import MongoClient

from app.settings.mongo_config import DB_URL

client = MongoClient(DB_URL)

db = client['global_terrorism_data']

events_collection = db['events']

regions_collection = db['regions']

country_collection = db['countries']