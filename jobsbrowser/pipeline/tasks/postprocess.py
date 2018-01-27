import requests

from celery.utils.log import get_task_logger

from .bases import MongoDBTask
from .. import app


logger = get_task_logger(__name__)


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


@app.task(base=MongoDBTask)
def post_to_stats_service(offer):
    """Post offer to stats service.

    Stats service URL is defined in celery settings.
    """
    collection = post_to_stats_service.mongodb.get_collection(
        app.conf.get('MONGO_RESULTS_COLLECTION'),
    )
    offer_id = offer['id']
    _offer = collection.find_one(
        {'offer_id': offer_id},
        projection={'_id': False},
    )
    try:
        response = requests.post(
            app.conf.get("STATS_SERVICE_ADD_URL"),
            json=dict(_offer)
        )
    except ConnectionError:
        logger.warning(
            f"Sending offer {offer_id} failed. "
            "Stats service is unavailable."
        )
    else:
        logger.info(
            f"Offer {offer_id} sent to stats service. "
            f"Returned Code: {response.status_code}"
        )
    return offer
