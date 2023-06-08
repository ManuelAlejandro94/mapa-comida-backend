from flask import request
from ...responses import ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/users', methods=['GET'])
    def get_users():
        """Endpoint que obtiene todos los usuarios"""
        response = []

        try:
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
            return Ok.with_results(
                code=0,
                message="Transacción exitosa",
                result=response
            )
        except Exception as e:
            raise e
        