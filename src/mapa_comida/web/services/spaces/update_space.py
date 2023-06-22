from flask import request
from src.mapa_comida.web.services.spaces import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/spaces/update-space/<id>', methods=['PUT'])
    def update_space(id):
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
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )
        if not busqueda_params["users"]:
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Parámetros vacíos", details="Campos: users") - HTTP 422')
            return BadRequest.with_results(
                error=-2,
                message="Parámetros vacíos",
                details="Campos: users"
            )
        if not busqueda_params["places"]:
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Parámetros vacíos", details="Campos: places") - HTTP 422')
            return BadRequest.with_results(
                error=-2,
                message="Parámetros vacíos",
                details="Campos: places"
            )
        
        place = {
            "id": id,
            "name": busqueda_params["name"],
            "users": busqueda_params["users"],
            "places": busqueda_params["places"]
        }

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_space_by_id: {id}')
            results = scouts.find_space_by_id(id)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-3, message="Espacio no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-3, message="Espacio no encontrado")
            else:
                app.logger.info(f'LOGID: {log_id} - Actualización update_space: {place}')
                scouts.update_space(place)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Lugar actualizado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Lugar actualizado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e