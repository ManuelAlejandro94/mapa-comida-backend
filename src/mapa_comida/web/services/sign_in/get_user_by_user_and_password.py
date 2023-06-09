from flask import request
from src.mapa_comida.web.services.sign_in import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/obtener-usuario', methods=['GET'])
    def get_user_by_user_and_password():
        busqueda_params = request.get_json()
        params = ["username", "password"]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)
        if dif_params:
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )
        
        username = busqueda_params["username"]
        password = busqueda_params["password"]

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_by_id_password: username={username}, password={password}')
            results = scouts.find_by_id_password(user=username, user_pass=password)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no encontrado con esos parámetros") - HTTP 422')
                return BadRequest.without_results(error=-2, message="Usuario no encontrado con esos parámetros")
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
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Coincidencia, result={user}") - HTTP 200')
                return Ok.with_results(code=0, message="Coincidencia", result=user)
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            error = {
                "codigo": str(e.error.value[0].value[0]) + "." + str(e.error.value[1]),
                "detalle": str(e.detalle),
                "mensaje": str(e.args[0])
            }
            raise error
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e
