from flask import request
from ..users import create_log_id
from ...responses import ResponseErrorBadRequest as BadRequest, ResponseOk

def register_routes(app, scouts):

    @app.route('/user', methods=['DELETE'])
    def delete_user():
        busqueda_params = request.get_json()
        log_id = create_log_id()

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_id: {busqueda_params["id"]}')
            results = scouts.find_user_id(busqueda_params["id"])
            app.logger.info(f'LOGID: {log_id} - Resultado búsqueda find_user_id: {results}')
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Usuario no encontrado")

            scouts.delete_user(busqueda_params["id"])

            app.logger.info(f'LOGID: {log_id} - Usuario {busqueda_params["id"]} eliminado con éxito - HTTP 200')
            return ResponseOk.without_results(code=0, message="Usuario eliminado con éxito")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            app.logger.error(e)
            raise e