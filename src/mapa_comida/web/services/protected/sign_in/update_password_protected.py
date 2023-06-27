from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.mapa_comida.web.services.protected.sign_in import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseErrorConflict as Conflict


def register_routes(app, scouts):

    @app.route('/sign-in/password/protected', methods=['PUT'])
    @jwt_required()
    def update_password_protected():
        current_user = get_jwt_identity()
        busqueda_params = request.get_json()
        params = [
            "password"
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
                password_params = {
                    "id": results["_id"],
                    "password": busqueda_params["password"]
                }
                app.logger.info(f'LOGID: {log_id} - Actualización update_password: {password_params}')
                scouts.update_password(password_params)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Contraseña actualizada correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Contraseña actualizada correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e