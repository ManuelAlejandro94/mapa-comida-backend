from src.mapa_comida.web.services.places import create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/place/<id>', methods=['GET'])
    def get_place_by_id(id):
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - ID del lugar: {id}')

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_place_by_id: {id}')
            result = scouts.find_place_by_id(id)
            if result is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Lugar no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Lugar no encontrado")
            
            place = {
                "id": str(result["_id"]),
                "name": result["name"],
                "created_by": result["created_by"],
                "cordenates": {
                    "latitud": result["cordenates"]["latitud"],
                    "longitud": result["cordenates"]["longitud"]
                },
                "address": result["address"],
                "created": result["created"],
                "updated": result["updated"]
            }
            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción correcta", result={place}) - HTTP 200')
            return Ok.with_results(code=0, message="Transacción correcta", result=place)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e