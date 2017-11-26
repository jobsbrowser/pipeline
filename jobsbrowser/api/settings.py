import os


class BaseConfig:
    DEBUG = False
    OFFERS_COLLECTION = 'offers'
    # MONGO_URI = 'mongodb://user:password@url:port/db_name'


class DevConfig(BaseConfig):
    DEBUG = True
    HOST = 'localhost'
    PORT = 5000
    MONGO_URI = 'mongodb://jobsbrowser:jobsbrowser@192.166.219.242:27447/jobsbrowser'


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True


CONFIG_MAPPING = {
    'DEV': DevConfig,
    'PRODUCTION': ProductionConfig,
    'TESTING': TestingConfig,
}


def get_config(config_name=None):
    config_name = config_name or os.environ.get('APP_CONFIG') or ""
    return CONFIG_MAPPING.get(config_name.upper(), DevConfig)
