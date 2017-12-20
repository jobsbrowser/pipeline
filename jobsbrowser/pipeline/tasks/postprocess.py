from .. import app
from .bases import MongoDBTask


@app.task(base=MongoDBTask)
def save_to_mongodb(offer):
    """Save offer to MongoDB.

    MongoDB URI and collection name are defined in celery settings.
    """
    save_to_mongodb.mongodb.get_collection(
        app.conf.get('MONGO_RESULTS_COLLECTION'),
    ).insert_one(offer)
    return offer
