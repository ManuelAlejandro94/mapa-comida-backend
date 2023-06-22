from flask import request
from src.mapa_comida.web.services.spaces import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/spaces/all-spaces', methods=['GET'])
    def get_spaces():
        log_id = create_log_id()
        response = []

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_spaces')
            results = scouts.find_spaces()

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
            
            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={response}) - HTTP 200')
            return Ok.with_results(
                code=0,
                message="Transacción exitosa",
                result=response
            )
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e