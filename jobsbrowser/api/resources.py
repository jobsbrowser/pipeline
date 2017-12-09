from datetime import date

from flask_pymongo import PyMongo
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
)

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
    # TODO: run tasks
    return jsonify({})


@pages_bp.route('/offers', methods=['GET'])
def get_offers():
    collection = mongo.db[current_app.config.get('OFFERS_COLLECTION')]
    offers_cursor = collection.find(
        {'valid_through': {'$gte': str(date.today())}},
    )
    return jsonify({'links': [offer['url'] for offer in offers_cursor]})
