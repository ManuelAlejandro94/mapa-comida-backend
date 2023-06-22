from flask import request
from src.mapa_comida.web.services.spaces import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/spaces/space/<id>', methods=['GET'])
    def get_space_by_id(id):
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - ID de entrada: {id}')

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_space_by_id: {id}')
            result = scouts.find_space_by_id(id_space=id)
            if result is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Espacio no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Espacio no encontrado")
            else:
                place = {
                    "id": str(result["_id"]),
                    "owner": result["owner"],
                    "name": result["name"],
                    "users": result["users"],
                    "places": result["places"],
                    "created": result["created"],
                    "updated": result["updated"]
                }
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={place}) - HTTP 200')
                return Ok.with_results(code=0, message="Transacción exitosa", result=place)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e