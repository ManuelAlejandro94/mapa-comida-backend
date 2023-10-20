from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.mapa_comida.web.services.protected.sign_in import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, \
    ResponseErrorConflict as Conflict, ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):
    @app.route('/sign-in/actualizar-correo', methods=['PUT'])
    @jwt_required()
    def update_email_protected():
        current_user = get_jwt_identity()
        busqueda_params = request.get_json()
        params = ["email"]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)
        email = busqueda_params["email"]
        if dif_params:
            app.logger.info(
                f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", '
                f'details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_username: {current_user}')
            results = scouts.find_user_by_username(current_user)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 422')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")
            else:
                app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_email: {email}')
                results_email = scouts.find_user_by_email(email)

                if results_email is not None:
                    app.logger.info(
                        f'LOGID: {log_id} - Conflict(error=-1, message="Correo registrado con anterioridad") - HTTP 422')
                    return Conflict.without_results(-1, "Correo registrado con anterioridad")
                # Actualizar email
                app.logger.info(f'LOGID: {log_id} - Actualización update_user_email: {email}')
                scouts.update_user_email(user_id=str(results["_id"]), user_email=email)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Email actualizado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Email actualizado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e
