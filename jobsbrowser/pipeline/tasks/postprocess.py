from .bases import MongoDBTask
from .. import app


@app.task(base=MongoDBTask)
def save_to_mongodb(offer):
    """Save offer to MongoDB.

    MongoDB URI and collection name are defined in celery settings.
    """
    save_to_mongodb.mongodb.get_collection(
        app.conf.get('MONGO_RESULTS_COLLECTION'),
    ).update_one(
        {'offer_id': offer['id']}, {'$set': {'tags': offer['tags']}}
    )
    return offer
