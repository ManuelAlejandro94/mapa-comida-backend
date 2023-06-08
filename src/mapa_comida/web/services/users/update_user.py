from flask import request
from ...responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok
from ..users import validate_params, create_log_id

def register_routes(app, scouts):

    @app.route('/user/<id>', methods=['PUT'])
    def update_user(id):
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
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_id: {id}')
            results = scouts.find_user_id(id)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Usuario no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-2, message="Usuario no encontrado")
            else:
                busqueda_params["id"] = id
                app.logger.info(f'LOGID: {log_id} - Actualización update_user: {busqueda_params}')
                scouts.update_user(busqueda_params)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Usuario actualizado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Usuario actualizado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e