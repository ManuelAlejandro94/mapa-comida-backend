from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import logging.config
from src.mapa_comida.web.services.users import get_users
from src.mapa_comida.scouts import Scouts


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

    mongodb_config =config.get('mongo')
    client = MongoClient(mongodb_config['host'])

    if mongodb_config['authentication'] is not None:
        auth_db = client.get_database(mongodb_config['authentication'])

        auth_db.authenticate(
            mongodb_config['user'],
            mongodb_config['pass']
        )

    database = client.get_database(mongodb_config['database'])
    collection = mongodb_config['collection']

    scouts = Scouts(
        database=database,
        collection=collection
    )

    get_users.register_routes(app, scouts)
    # new_client.register_routes(app, scouts)
    # update_client.register_routes(app, scouts)
    # delete_client.register_routes(app, scouts)

    return app
