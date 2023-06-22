from flask import request
from src.mapa_comida.web.services.places import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/place/<id>', methods=['PUT'])
    def update_place(id):
        busqueda_params = request.get_json()
        params = [
            "name",
            "cordenates",
            "address"
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
        else:
            cordenate_params = ["latitud", "longitud"]
            dif_cordenates = validate_params(params=cordenate_params, request=busqueda_params["cordenates"])
            if dif_cordenates:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
                return BadRequest.with_results(
                    error=-1,
                    message="Parámetros faltantes en la petición",
                    details=f"Campos: {dif_params}"
                )
        
        #Aquí me quedé, validar campos a actualizar antes de mandar al scout a actualizar
        scout_params = {
            "id": id,
            "name": busqueda_params["name"],
            "address": busqueda_params["address"],
            "cordenates": {
                "latitud": busqueda_params["cordenates"]["latitud"],
                "longitud": busqueda_params["cordenates"]["longitud"]
            }
        }

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_place_by_id: {id}')
            results = scouts.find_place_by_id(id)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Lugar no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-2, message="Lugar no encontrado")
            else:
                app.logger.info(f'LOGID: {log_id} - Actualización update_place: {scout_params}')
                scouts.update_place(scout_params)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Lugar actualizado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Lugar actualizado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e