from flask import request

def register_routes(app, scouts):

    @app.route('/user', methods=['POST'])
    def new_user():
        busqueda_params = request.get_json()

        try:
            results = scouts.find_user_by_email(busqueda_params["email"])
            if results is not None:
                return {
                    "error_code": -1,
                    "messsage": "Correo registrado con anterioridad"
                }, 422
            
            #salt = bcrypt.gensalt()
            #hashed = bcrypt.hashpw(busqueda_params["password"])
            scouts.create_user(busqueda_params)

            return {
                "code": 0,
                "message": "Usuario agregado con éxito"
            }, 201
        except Exception as e:
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            raise e