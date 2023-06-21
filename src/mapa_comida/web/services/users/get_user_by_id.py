from src.mapa_comida.web.services.sign_in import create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/users/<id>', methods=['GET'])
    def get_user_by_id(id):
        log_id = create_log_id()

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_id: {id}')
            results = scouts.find_user_id(user_id=id)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Usuario no encontrado")
            else:
                user = {
                    "id": str(results["_id"]),
                    "username": results["username"],
                    "email": results["email"],
                    "password": results["password"],
                    "name": results["name"],
                    "lastname": results["lastname"],
                    "created": results["created"],
                    "last_updated": results["last_updated"],
                    "pass_updated": results["pass_updated"]
                }
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result={user}) - HTTP 200')
                return Ok.with_results(code=0, message="Transacción exitosa", result=user)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e