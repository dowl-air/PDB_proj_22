from flask import Flask


def create_app(config_name):
    """Create app factory

    Keyword arguments:
    config_name -- Type of config used to work with created app. (development, testing, production)
    Return: app
    """

    app = Flask(__name__)

    config_module = f"app.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    return app
