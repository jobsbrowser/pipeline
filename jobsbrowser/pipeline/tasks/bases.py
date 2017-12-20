from pymongo import MongoClient

from .. import app
from .utils import lower_word_tokenize


class MongoDBTask(app.Task):
    _mongodb = None

    @property
    def mongodb(self):
        if self._mongodb is None:
            self._mongodb = MongoClient(app.conf.get('MONGO_URI'))
        return self._mongodb.get_database()


class TagsFindingTask(MongoDBTask):
    SENTINEL = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags_dict = self._build_tags_dict()

    def _get_tags(self):
        return self.mongodb["tags"]

    def _build_tags_dict(self):
        tags_dict = {}
        for tag in self._get_tags():
            for tag_name in [tag["name"]] + tag.get("synonyms", []):
                tag_dict = tags_dict
                for token in lower_word_tokenize(tag_name):
                    tag_dict = tag_dict.setdefault(token, {})
                tag_dict[self.SENTINEL] = tag["name"]
        return tags_dict

    def find_tags(self, offer):
        offer_tags = []

        stack = []
        for token in offer["description"]:
            new_stack = []
            for tag_dict in stack:
                if token in tag_dict:
                    new_stack.append(tag_dict[token])
                if self.SENTINEL in tag_dict:
                    offer_tags.append(tag_dict[self.SENTINEL])
            if token in self.tags_dict:
                new_stack.append(self.tags_dict[token])
            stack = new_stack

        offer["tags"] = offer_tags
        return offer
