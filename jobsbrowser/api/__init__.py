from flask import Flask

from .settings import get_config
from .resources import (
    mongo,
    pages_bp,
)

__all__ = ['init_app']


def init_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    mongo.init_app(app)
    app.register_blueprint(pages_bp)
    return app
