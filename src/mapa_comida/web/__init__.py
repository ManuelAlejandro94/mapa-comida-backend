import datetime

from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import logging.config
from src.mapa_comida.web.services.users import get_users, new_user, delete_user, update_user, get_user_by_id
from src.mapa_comida.web.services.protected.users import get_user_by_username, update_user_protected
from src.mapa_comida.web.services.sign_in import update_password, get_user_by_user_and_password, update_email
from src.mapa_comida.web.services.places import new_place, get_places, get_place_by_id, update_place, delete_place
from src.mapa_comida.web.services.spaces import get_spaces, new_space, update_space, delete_space, get_space_by_id, \
    get_spaces_by_owner, get_spaces_member
from src.mapa_comida.web.services.tokenizer import login
from src.mapa_comida.web.services.protected.sign_in import update_email_protected
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

    # region tjwt
    token_config = config.get('token')
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = token_config['SECRET-KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=token_config['EXPIRES'])
    # endregion

    mongodb_config = config.get('mongo')
    client = MongoClient(mongodb_config['host'])

    if mongodb_config['authentication'] is not None:
        uri = f"mongodb+srv://{mongodb_config['user']}:{mongodb_config['pass']}@{mongodb_config['host']}/"
        client = MongoClient(uri)

    database = client.get_database(mongodb_config['database'])
    collection = mongodb_config['collection']
    collection_places = mongodb_config['collection_places']
    collection_spaces = mongodb_config['collection_spaces']

    scouts = Scouts(
        database=database,
        collection=collection,
        collection_places=collection_places,
        collection_spaces=collection_spaces
    )

    # region Endpoints
    # region User
    get_users.register_routes(app, scouts)
    new_user.register_routes(app, scouts)
    delete_user.register_routes(app, scouts)
    update_user.register_routes(app, scouts)
    get_user_by_id.register_routes(app, scouts)
    # endregion
    # region Sign in
    update_password.register_routes(app, scouts)
    get_user_by_user_and_password.register_routes(app, scouts)
    update_email.register_routes(app, scouts)
    # endregion
    # region Place
    get_places.register_routes(app, scouts)
    new_place.register_routes(app, scouts)
    get_place_by_id.register_routes(app, scouts)
    update_place.register_routes(app, scouts)
    delete_place.register_routes(app, scouts)
    # endregion
    # region Space
    get_spaces.register_routes(app, scouts)
    new_space.register_routes(app, scouts)
    update_space.register_routes(app, scouts)
    delete_space.register_routes(app, scouts)
    get_space_by_id.register_routes(app, scouts)
    get_spaces_by_owner.register_routes(app, scouts)
    get_spaces_member.register_routes(app, scouts)
    # endregion
    # region Tokenizer
    login.register_routes(app, scouts)
    # endregion
    # endregion

    # region Protected
    # region User
    get_user_by_username.register_routes(app, scouts)
    update_user_protected.register_routes(app, scouts)
    # endregion
    # region Sign in
    update_email_protected.register_routes(app, scouts)
    # endregion
    # endregion

    return app
