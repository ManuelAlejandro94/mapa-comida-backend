from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import logging.config
from src.mapa_comida.web.services.users import get_users, new_user, delete_user, update_user, get_user_by_id
from src.mapa_comida.web.services.sign_in import update_password, get_user_by_user_and_password, update_email
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

    mongodb_config =config.get('mongo')
    client = MongoClient(mongodb_config['host'])

    if mongodb_config['authentication'] is not None:
        uri = f"mongodb+srv://{mongodb_config['user']}:{mongodb_config['pass']}@{mongodb_config['host']}/"
        client = MongoClient(uri)

    database = client.get_database(mongodb_config['database'])
    collection = mongodb_config['collection']
    collection_places = mongodb_config['collection_places']

    scouts = Scouts(
        database=database,
        collection=collection,
        collection_places=collection_places
    )

    #region Endpoints
    #region User
    get_users.register_routes(app, scouts)
    new_user.register_routes(app, scouts)
    delete_user.register_routes(app, scouts)
    update_user.register_routes(app, scouts)
    get_user_by_id.register_routes(app, scouts)
    #endregion
    #region Sign in
    update_password.register_routes(app, scouts)
    get_user_by_user_and_password.register_routes(app, scouts)
    update_email.register_routes(app, scouts)
    #endregion
    #region Place
    #endregion
    #endregion

    return app
