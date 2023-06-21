from flask import request
from src.mapa_comida.web.services.places import create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/places', methods=['GET'])
    def get_places():
        log_id = create_log_id()
        response = []

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_all_places')
            results = scouts.find_all_places()

            for result in results:
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
                response.append(place)

            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={response}) - HTTP 200')
            return Ok.with_results(
                code=0,
                message="Transacción exitosa",
                result=response
            )
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e