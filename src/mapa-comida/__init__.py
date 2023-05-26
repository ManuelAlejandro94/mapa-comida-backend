from flask import Flask
from flask_cors import CORS
import logging.config


def logging_config(config):
    if config:
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.DEBUG)


def create_application(config):
    logging.debug("Creando aplicación")

    logging_config(config.get('logging'))

    app = Flask(__name__)
    cors = CORS(app)

    # mysql_config = config.get('mysql')
    #
    # scouts = Scouts(
    #     database=mysql_config
    # )
    #
    # get_clients.register_routes(app, scouts)
    # new_client.register_routes(app, scouts)
    # update_client.register_routes(app, scouts)
    # delete_client.register_routes(app, scouts)

    return app
