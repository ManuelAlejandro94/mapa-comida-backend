from flask import request
from src.mapa_comida.web.services.spaces import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/spaces/member/<id>', methods=['GET'])
    def get_spaces_member(id):
        log_id = create_log_id()
        response = []
        app.logger.info(f'LOGID: {log_id} - ID de entrada: {id}')

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_spaces_member: {id}')
            results = scouts.find_spaces_member(id)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no pertenece a ningún espacio") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Usuario no pertenece a ningún espacio")
            else:
                for result in results:
                    place = {
                        "id": str(result["_id"]),
                        "owner": result["owner"],
                        "name": result["name"],
                        "users": result["users"],
                        "places": result["places"],
                        "created": result["created"],
                        "updated": result["updated"]
                    }
                    response.append(place)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa") - HTTP 200')
                return Ok.with_results(code=0, message="Transacción exitosa", result=response)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e