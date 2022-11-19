from .create_app import create_app
from .settings import config

application = create_app()

if config.FLASK_CONFIG == "development":
    application.run(host=config.HOST, port=config.PORT, debug=True)
else:
    application.run(host=config.HOST, port=config.PORT, debug=False)
