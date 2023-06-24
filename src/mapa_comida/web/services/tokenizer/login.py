import hashlib

from flask import request
from flask_jwt_extended import create_access_token

from src.mapa_comida.web.services.tokenizer import validate_params, create_log_id
from src.mapa_comida.web.responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseErrorAuthentication as ErrorAuthentication


def register_routes(app, scouts):
    @app.route('/tokenizer-login', methods=['POST'])
    def login():
        busqueda_params = request.get_json()
        params = [
            "email",
            "password"
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

        login_params = {
            "email": busqueda_params["email"],
            "password": busqueda_params["password"]
        }

        try:
            app.logger.info(f'LOGID: {log_id} - Búsqueda find_user_by_email: {login_params["email"]}')
            results = scouts.find_user_by_email(login_params["email"])
            if results is None:
                app.logger.info(f'LOGID: {log_id} - ErrorAuthentication(error=-1, message="Correo o contraseña incorrecta") - HTTP 401')
                return ErrorAuthentication.without_results(error=-1, message="Correo o contraseña incorrecta")
            else:
                encrypted_password = hashlib.sha512(login_params["password"].encode("utf-8")).hexdigest()
                passwd = results["password"]
                username = results["username"]
                if encrypted_password == passwd:
                    access_token = create_access_token(identity=username)
                    response = {"access_token": access_token}
                    app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Token creado exitosamente", result={response}) - HTTP 200')
                    return Ok.with_results(code=0, message="Token creado exitosamente", result=response)

            app.logger.info(f'LOGID: {log_id} - ErrorAuthenthication(error=-1, message="Correo o contraseña incorrecta") - HTTP 401')
            return ErrorAuthentication.without_results(error=-1, message="Correo o contraseña incorrecta")
        except Exception as e:
            app.logger.error(f'LOGID: {log_id} - Error: {e}')
            raise e
