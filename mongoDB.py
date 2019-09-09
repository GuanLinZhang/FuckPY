from pymongo import MongoClient


def conn():
    client = MongoClient()
    db = client.test
    return db

