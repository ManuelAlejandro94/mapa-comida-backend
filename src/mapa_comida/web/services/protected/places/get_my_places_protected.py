from flask_jwt_extended import jwt_required, get_jwt_identity
from src.mapa_comida.web.services.protected.places import create_log_id
from src.mapa_comida.web.responses import ResponseOk as Ok, ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):
    @app.route('/all-my-places/protected', methods=['GET'])
    @jwt_required()
    def get_my_places_protected():
        current_user = get_jwt_identity()
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {current_user}')

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_username: {current_user}')
            results = scouts.find_user_by_username(username=current_user)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 401')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")

            app.logger.info(f'LOGID: {log_id} - Búsqueda find_place_by_owner: {str(results["_id"])}')
            response = []
            results_place = scouts.find_place_by_owner(str(results["_id"]))
            for result in results_place:
                place = {
                    "id": str(result["_id"]),
                    "name": result["name"],
                    "created_by": result["created_by"],
                    "cordenates": result["cordenates"],
                    "address": result["address"],
                    "created": result["created"],
                    "updated": result["updated"]
                }
                response.append(place)
            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={response}) - HTTP 200')
            return Ok.with_results(code=0, message="Transacción exitosa", result=response)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e