from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.mapa_comida.web.services.protected.places import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, \
    ResponseErrorConflict as Conflict, ResponseErrorAuthentication as ErrorAuth


def register_routes(app, scouts):
    @app.route('/place-new/protected', methods=['POST'])
    @jwt_required()
    def new_place_protected():
        current_user = get_jwt_identity()
        busqueda_params = request.get_json()
        params = [
            "name",
            "cordenates",
            "address"
        ]
        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {busqueda_params}')
        dif_params = validate_params(params=params, request=busqueda_params)
        if dif_params:
            app.logger.info(
                f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Parámetros faltantes en la petición",
                details=f"Campos: {dif_params}"
            )
        else:
            cordenate_params = ["latitud", "longitud"]
            dif_cordenates = validate_params(params=cordenate_params, request=busqueda_params["cordenates"])
            if dif_cordenates:
                app.logger.info(
                    f'LOGID: {log_id} - BadRequest(error=-1, message="Parámetros faltantes en la petición", details="Campos: {dif_params}") - HTTP 422')
                return BadRequest.with_results(
                    error=-1,
                    message="Parámetros faltantes en la petición",
                    details=f"Campos: {dif_params}"
                )

        cordenates = busqueda_params["cordenates"]

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_username: {current_user}')
            results = scouts.find_user_by_username(username=current_user)
            if results is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuth(error=-1, message="Usuario no encontrado") - HTTP 401')
                return ErrorAuth.without_results(error=-1, message="Usuario no encontrado")

            app.logger.info(f'LOGID: {log_id} - Búsqueda find_place_by_cordenates: {cordenates}')
            results_cordenates = scouts.find_place_by_cordenates(cordenates)
            if results_cordenates is None:
                app.logger.info(f'LOGID: {log_id} - Conflict(error=-1, message="Lugar ya existe") - HTTP 409')
                return Conflict.without_results(error=-2, message="Lugar ya existe")
            else:
                place_params = {
                    "name": busqueda_params["name"],
                    "created_by": str(results["_id"]),
                    "cordenates": cordenates,
                    "address": busqueda_params["address"]
                }
                app.logger.info(f'LOGID: {log_id} - Creación create_place: {place_params}')
                scouts.create_place(place_params)
                app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Lugar agregado correctamente") - HTTP 200')
                return Ok.without_results(code=0, message="Lugar agregado correctamente")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e