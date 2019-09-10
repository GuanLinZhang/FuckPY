from pymongo import MongoClient


class ConnectionHelper(object):
    __db = None

    @classmethod
    def conn(cls):
        if cls.__db is None:
            cls.__db = MongoClient().test
        return cls.__db
