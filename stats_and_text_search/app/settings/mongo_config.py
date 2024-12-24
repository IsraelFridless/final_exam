from pymongo import MongoClient


DB_URL = 'mongodb://172.17.242.253:27017'

client = MongoClient(DB_URL)

db = client['global_terrorism_data']

events_collection = db['events']

region_collection = db['regions']

country_collection = db['countries']