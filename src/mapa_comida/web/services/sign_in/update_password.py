from flask import request

def register_routes(app, scouts):

    @app.route('/password/<id>', methods=['PUT'])
    def update_password(id):
        busqueda_params = request.get_json()

        try:
            results = scouts.find_user_id(id)
            if results is None:
                return {
                    "error_code": -1,
                    "message": "Usuario no encontrado"
                }, 422
            else:
                busqueda_params["id"] = id
                scouts.update_password(busqueda_params)
                return {
                    "code": 0,
                    "message": "Contraseña actualizada correctamente"
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