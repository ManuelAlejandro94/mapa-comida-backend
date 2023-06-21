from flask import request
from ..users import validate_params, create_log_id
from ...responses import ResponseErrorBadRequest as BadRequest, CreatedOk as Ok

def register_routes(app, scouts):

    @app.route('/user', methods=['POST'])
    def new_user():
        busqueda_params = request.get_json()
        params = [
            "username",
            "email",
            "password",
            "name",
            "lastname"
        ]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)
        if dif_params:
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message=""Parámetros faltantes en la petición, details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_email: {busqueda_params["email"]}')
            results = scouts.find_user_by_email(busqueda_params["email"])
            if results is not None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Correo registrado con anterioridad") - HTTP 422')
                return BadRequest.without_results(-2, "Correo registrado con anterioridad")
            
            app.logger.info(f'LOGID: {log_id} - Crea create_user: {busqueda_params}')
            scouts.create_user(busqueda_params)

            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Usuario agregadi con éxito") - HTTP 201')
            return Ok.without_results(0, "Usuario agregado con éxito")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e