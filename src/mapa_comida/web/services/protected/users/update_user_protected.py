from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseErrorConflict as Conflict
from src.mapa_comida.web.services.protected.users import validate_params, create_log_id


def register_routes(app, scouts):

    @app.route('/user/update-user-names', methods=['PUT'])
    @jwt_required()
    def update_user_protected():
        current_user = get_jwt_identity()
        busqueda_params = request.get_json()
        params = [
            "name",
            "lastname"
        ]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)

        if dif_params:
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_username: {current_user}')
            results = scouts.find_user_by_username(current_user)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - Conflict(error=-1, message="Usuario no encontrado") - HTTP 409')
                return Conflict.without_results(error=-1, message="Usuario no encontrado")
            else:
                update_params = {
                    "id": str(results["_id"]),
                    "name": busqueda_params["name"],
                    "lastname": busqueda_params["lastname"]
                }
                app.logger.info(f'LOGID: {log_id} - Actualización update_user: {update_params}')
                scouts.update_user(update_params)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Usuario actualizado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Usuario actualizado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e