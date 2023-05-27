from flask import request

def register_routes(app, scouts):

    @app.route('/user', methods=['DELETE'])
    def delete_user():
        busqueda_params = request.get_json()

        try:
            results = scouts.find_user_id(busqueda_params["id"])
            if results is None:
                return {
                    "error_code": -1,
                    "messsage": "Usuario no encontrado"
                }, 422

            scouts.delete_user(busqueda_params["id"])

            return {
                "code": 0,
                "message": "Usuario eliminado con éxito"
            }, 200
        except Exception as e:
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            raise e