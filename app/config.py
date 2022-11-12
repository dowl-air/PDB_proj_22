class Config(object):
    """ Base configuration"""

class DevelopmentConfig(Config):
    """ Development configuration """
    DEVELOPMENT = True

class TestingConfig(Config):
    """ Testing configuration """
    TESTING = True

class ProductionConfig(Config):
    """ Production configuration """
    PRODUCTION = True