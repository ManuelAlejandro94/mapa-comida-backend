from flask import request
from ...responses import ResponseErrorBadRequest as BadRequest, ResponseOk

def register_routes(app, scouts):

    @app.route('/user', methods=['DELETE'])
    def delete_user():
        busqueda_params = request.get_json()

        try:
            results = scouts.find_user_id(busqueda_params["id"])
            if results is None:
                return BadRequest.without_results(error=-1, message="Usuario no encontrado")

            scouts.delete_user(busqueda_params["id"])

            return ResponseOk.without_results(code=0, message="Usuario eliminado con éxito")
        except Exception as e:
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            raise e