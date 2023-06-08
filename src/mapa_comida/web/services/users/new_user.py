from flask import request
from ..users import validate_params
from ...responses import ResponseErrorBadRequest as BadRequest, CreatedOk as Ok

def register_routes(app, scouts):

    @app.route('/user', methods=['POST'])
    def new_user():
        busqueda_params = request.get_json()
        params = [
            "username",
            "email",
            "password",
            "name",
            "lastname"
        ]
        dif_params = validate_params(params=params, request=busqueda_params)
        if dif_params:
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )

        try:
            results = scouts.find_user_by_email(busqueda_params["email"])
            if results is not None:
                return BadRequest.without_results(-2, "Correo registrado con anterioridad")
            
            #salt = bcrypt.gensalt()
            #hashed = bcrypt.hashpw(busqueda_params["password"])
            scouts.create_user(busqueda_params)

            return Ok.without_results(0, "Usuario agregado con éxito")
        except Exception as e:
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            raise e