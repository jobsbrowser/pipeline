import json

from pymongo import MongoClient

from . import app


class MongoDBTask(app.Task):
    _mongodb = None

    @property
    def mongodb(self):
        # tags = []
        # with open('tags.jl') as f:
        #     for line in f:
        #         tag = json.loads(line)
        #         tag["name"] = tag["name"].replace("-", " ")
        #         tags.append(json.loads(line))
        # return {"tags": tags}
        if self._mongodb is None:
            self._mongodb = MongoClient(app.conf.get('MONGO_URI'))
        return self._mongodb.get_database()
