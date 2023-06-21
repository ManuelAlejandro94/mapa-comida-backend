from flask import request
from src.mapa_comida.web.services.sign_in import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/password/<id>', methods=['PUT'])
    def update_password(id):
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
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user: {id}')
            results = scouts.find_user_id(id)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-2, message="Usuario no encontrado")
            else:
                busqueda_params["id"] = id
                app.logger.info(f'LOGID: {log_id} - Actualización update_password: {busqueda_params}')
                scouts.update_password(busqueda_params)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Contraseña actualizada correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Contraseña actualizada correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e