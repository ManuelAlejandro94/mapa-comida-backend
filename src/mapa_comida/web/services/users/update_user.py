from flask import request
from ...responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok
from ..users import validate_params

def register_routes(app, scouts):

    @app.route('/user/<id>', methods=['PUT'])
    def update_user(id):
        busqueda_params = request.get_json()
        params = [
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
            results = scouts.find_user_id(id)
            if results is None:
                return BadRequest.without_results(error=-2, message="Usuario no encontrado")
            else:
                busqueda_params["id"] = id
                scouts.update_user(busqueda_params)
                return Ok.without_results(code=0, message="Usuario actualizado correctamente")
        except Exception as e:
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            raise e