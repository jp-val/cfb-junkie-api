from app import app
from flask_pymongo import PyMongo

mongo_client = PyMongo(app)
db = mongo_client.db