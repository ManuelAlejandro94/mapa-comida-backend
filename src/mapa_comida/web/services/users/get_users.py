from flask import request
from ...responses import ResponseOk as Ok
from src.mapa_comida.web.services.users import create_log_id

def register_routes(app, scouts):

    @app.route('/users', methods=['GET'])
    def get_users():
        """Endpoint que obtiene todos los usuarios"""
        response = []
        log_id = create_log_id()

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_users')
            results = scouts.find_users()
            
            for result in results:
                user = {
                    "id": str(result["_id"]),
                    "username": result["username"],
                    "email": result["email"],
                    "password": result["password"],
                    "name": result["name"],
                    "lastname": result["lastname"],
                    "created": result["created"],
                    "last_updated": result["last_updated"],
                    "pass_updated": result["pass_updated"]
                }
                response.append(user)
            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Transacción exitosa", result=response) - HTTP 200')
            return Ok.with_results(
                code=0,
                message="Transacción exitosa",
                result=response
            )
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e
        