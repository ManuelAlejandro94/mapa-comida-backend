from flask_jwt_extended import jwt_required, get_jwt_identity
from src.mapa_comida.web.services.spaces import create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, \
    ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):

    @app.route('/own-spaces', methods=['GET'])
    @jwt_required()
    def get_spaces_by_owner_protected():
        current_user = get_jwt_identity()
        log_id = create_log_id()
        response = []
        app.logger.info(f'LOGID: {log_id} - Usuario de entrada: {current_user}')

        try:
            results_user = scouts.find_user_by_username(username=current_user)
            if results_user is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 401')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")

            app.logger.info(f'LOGID: {log_id} - Búsqueda find_spaces_by_owner: {str(results_user["_id"])}')
            results = scouts.find_spaces_by_owner(str(results_user["_id"]))
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no tiene espacios") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Usuario no tiene espacios")
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
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={response}) - HTTP 200')
                return Ok.with_results(code=0, message="Transacción exitosa", result=response)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e