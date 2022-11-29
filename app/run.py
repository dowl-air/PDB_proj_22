from create_app import create_app
from appconfig import get_env_file_config

config = get_env_file_config()

application = create_app()

if config.FLASK_CONFIG == "development":
    application.run(host=config.HOST, port=config.PORT, debug=True)
else:
    application.run(host=config.HOST, port=config.PORT, debug=False)
