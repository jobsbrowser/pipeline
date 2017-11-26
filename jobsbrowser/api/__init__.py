from flask import Flask

from .settings import get_config
from .resources import (
    mongo,
    pages_bp,
)

__all__ = ['init_app']


def init_app(config_name=None, init_extensions=True):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    app.register_blueprint(pages_bp)
    if init_extensions:
        mongo.init_app(app)
    return app
