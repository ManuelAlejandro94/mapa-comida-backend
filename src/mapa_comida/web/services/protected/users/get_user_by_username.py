from flask_jwt_extended import jwt_required, get_jwt_identity
from src.mapa_comida.web.services.protected.users import create_log_id
from src.mapa_comida.web.responses import ResponseOk as Ok, ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):
    @app.route('/users/user', methods=['GET'])
    @jwt_required()
    def get_user_by_username():
        current_user = get_jwt_identity()
        log_id = create_log_id()

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_username: {current_user}')
            results = scouts.find_user_by_username(username=current_user)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 401')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")
            else:
                user = {
                    "id": str(results["_id"]),
                    "username": results["username"],
                    "email": results["email"],
                    "password": results["password"],
                    "name": results["name"],
                    "lastname": results["lastname"],
                    "created": results["created"],
                    "last_updated": results["last_updated"],
                    "pass_updated": results["pass_updated"]
                }
                app.logger.info(
                    f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={user}) - HTTP 200')
                return Ok.with_results(code=0, message="Transacción exitosa", result=user)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e
