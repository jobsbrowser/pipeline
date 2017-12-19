from pymongo import MongoClient

from . import app


class MongoDBTask(app.Task):
    _mongodb = None

    @property
    def mongodb(self):
        if self._mongodb is None:
            self._mongodb = MongoClient(app.conf.get('MONGO_URI'))
        return self._mongodb.get_default_database()
