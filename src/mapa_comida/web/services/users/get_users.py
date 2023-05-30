from flask import request

def register_routes(app, scouts):

    @app.route('/users', methods=['GET'])
    def get_users():
        multimap = request.args if request.method == 'GET' else request.form

        response = []
        error = None

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
            return response
        except Exception as e:
            raise e
        