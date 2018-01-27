from datetime import date

from flask_pymongo import PyMongo
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
)

from jobsbrowser.pipeline.chains import pracuj_pipeline

pages_bp = Blueprint('pages', __name__)
mongo = PyMongo()


@pages_bp.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@pages_bp.route('/offers', methods=['POST'])
def add_offer():
    offer = request.get_json()
    mongo_collection = mongo.db[current_app.config.get('OFFERS_COLLECTION')]
    mongo_collection.find_one_and_replace(
        {'url': offer['url']},
        offer,
        upsert=True,
    )
    pracuj_pipeline(offer)
    return jsonify({})


@pages_bp.route('/offers', methods=['GET'])
def get_offers():
    collection = mongo.db[current_app.config.get('OFFERS_COLLECTION')]
    offers_cursor = collection.find(
        {'valid_through': {'$gte': str(date.today())}},
    )
    return jsonify({'links': [offer['url'] for offer in offers_cursor]})


@pages_bp.route('/offers', methods=['PUT'])
def update_offer():
    category_key = 'categories'
    offer = request.get_json()
    url = offer['url']
    mongo_collection = mongo.db[current_app.config.get('OFFERS_COLLECTION')]
    query_result = mongo_collection.find_one(
        {'url': url},
        projection={category_key: True},
    )
    if query_result is None:
        return jsonify({}), 404
    if offer.get(category_key):
        offer[category_key] = list({
            offer[category_key],
            *query_result[category_key],
        })
    mongo_collection.update_one({'url': url}, {'$set': offer})
    return jsonify({})
