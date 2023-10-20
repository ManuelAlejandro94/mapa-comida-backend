from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.mapa_comida.web.services.spaces import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, \
    ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):
    @app.route('/create-own-space', methods=['POST'])
    @jwt_required()
    def new_space_protected():
        current_user = get_jwt_identity()
        busqueda_params = request.get_json()
        params = [
            "name",
            "users",
            "places"
        ]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)
        if dif_params:
            app.logger.info(
                f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )

        try:
            results_user = scouts.find_user_by_username(username=current_user)
            if results_user is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 401')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")

            users = []
            if not busqueda_params["users"]:
                users.append(str(results_user["_id"]))
            else:
                users = busqueda_params
                if str(results_user["_id"]) not in busqueda_params["users"]:
                    users.append(str(results_user["_id"]))

            place = {
                "name": busqueda_params["name"],
                "owner": str(results_user["_id"]),
                "users": users,
                "places": busqueda_params["places"]
            }

            app.logger.info(f'LOGID: {log_id} - Creación create_space: {place}')
            scouts.create_space(place)
            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Espacio creado correctamente") - HTTP 200')
            return Ok.without_results(code=0, message="Espacio creado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e
