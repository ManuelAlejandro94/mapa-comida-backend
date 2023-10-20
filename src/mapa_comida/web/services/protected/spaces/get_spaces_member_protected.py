from flask_jwt_extended import jwt_required, get_jwt_identity

from src.mapa_comida.web.services.spaces import create_log_id
from src.mapa_comida.web.responses import ResponseErrorConflict as Conflict, ResponseOk as Ok, \
    ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):

    @app.route('/member-spaces', methods=['GET'])
    @jwt_required()
    def get_spaces_member_protected():
        current_user = get_jwt_identity()
        log_id = create_log_id()
        response = []
        app.logger.info(f'LOGID: {log_id} - Usuario de entrada: {current_user}')

        try:
            results_user = scouts.find_user_by_username(username=current_user)
            if results_user is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 401')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")

            app.logger.info(f'LOGID: {log_id} - Búsqueda find_spaces_member: {str(results_user["_id"])}')
            results = scouts.find_spaces_member(str(results_user["_id"]))
            if results is None:
                app.logger.info(f'LOGID: {log_id} - Conflict(error=-1, message="Usuario no pertenece a ningún espacio") - HTTP 422')
                return Conflict.without_results(error=-1, message="Usuario no pertenece a ningún espacio")
            else:
                for result in results:
                    place = {
                        "id": str(result["_id"]),
                        "owner": result["owner"],
                        "name": result["name"],
                        "users": result["users"],
                        "places": result["places"],
                        "created": result["created"],
                        "updated": result["updated"]
                    }
                    response.append(place)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa") - HTTP 200')
                return Ok.with_results(code=0, message="Transacción exitosa", result=response)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e