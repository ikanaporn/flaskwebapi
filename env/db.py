
from flask import Flask
from flask_pymongo import pymongo
from app import app


#mongo = pymongo.MongoClient('mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net/Images', maxPoolSize=50, connect=False)
CONNECTION_STRING = "mongodb+srv://ikanaporn:Com75591;@cluster0.x8seg.mongodb.net/Images?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
Unknown = pymongo.collection.Collection(db, 'Unknown')