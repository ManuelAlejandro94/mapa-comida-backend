from flask import request
from src.mapa_comida.web.services.places import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/place', methods=['DELETE'])
    def delete_place():
        busqueda_params = request.get_json()
        params = ["id"]
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
        
        id_place = busqueda_params["id"]
        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_place_by_id: {id_place}')
            results = scouts.find_place_by_id(id_place)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Lugar no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-2, message="Lugar no encontrado")
            
            app.logger.info(f'LOGID: {log_id} - Eliminación delete_place: {id_place}')
            scouts.delete_place(id_place)
            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Lugar eliminado correctamente") - HTTP 200')
            return Ok.without_results(code=0, message="Lugar eliminado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e