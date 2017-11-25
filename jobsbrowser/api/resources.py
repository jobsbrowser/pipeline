from datetime import date

from flask import (
    Flask,
    jsonify,
    request,
)
from flask_pymongo import PyMongo

from .settings import get_config


def init_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    app.mongo = PyMongo(app)
    return app


app = init_app()


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/offers', methods=['POST'])
def add_offer():
    offer = request.get_json()
    mongo_collection = app.mongo.db[app.config.get('OFFERS_COLLECTION')]
    mongo_collection.find_one_and_replace(
        {'url': offer['url']},
        offer,
        upsert=True,
    )
    # TODO: run luigi task
    return jsonify({})


@app.route('/offers', methods=['GET'])
def get_offers():
    collection = app.mongo.db[app.config.get('OFFERS_COLLECTION')]
    offers_cursor = collection.find(
        {'valid_through': {'$gte': str(date.today())}},
    )
    return jsonify([offer['url'] for offer in offers_cursor])
