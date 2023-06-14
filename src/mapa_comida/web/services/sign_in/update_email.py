from flask import request
from src.mapa_comida.web.services.sign_in import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok

def register_routes(app, scouts):

    @app.route('/actualizar-correo', methods=['PUT'])
    def update_email():
        busqueda_params = request.get_json()
        params = ["id", "email"]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)
        id = busqueda_params["id"]
        email = busqueda_params["email"]
        if dif_params:
            app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_id: {busqueda_params["id"]}')
            results = scouts.find_user_id(busqueda_params["id"])
            if results is None:
                app.logger.info(f'LOGID: {log_id} - BadRequest(error=-1, message="Usuario no encontrado") - HTTP 422')
                return BadRequest.without_results(error=-1, message="Usuario no encontrado")
            else:
                #Validar si existe el nuevo email, en caso de que exista mandamos mensaje de que ya existe, en caso de que no pasamos a actualizar email
                app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_email: {busqueda_params}')
                results_email = scouts.find_user_by_email(email)

                if results_email is not None:
                    app.logger.info(f'LOGID: {log_id} - BadRequest(error=-2, message="Correo registrado con anterioridad") - HTTP 422')
                    return BadRequest.without_results(-2, "Correo registrado con anterioridad")
                #Actualizar email
                app.logger.info(f'LOGID: {log_id} - Actualización update_user_email: {busqueda_params}')
                scouts.update_user_email(user_id=id, user_email = email)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Email actualizado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Email actualizado correctamente")
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