class ResponseOk:

    def without_results(code, message):
        response = {
            "code": code,
            "message": message
        }, 200
        return response
    
    def with_results(code, message, result):
        response = {
            "code": code,
            "message": message,
            "response": result
        }, 200
        return response

class CreatedOk:
    
    def without_results(code, message):
        response = {
            "code": code,
            "message": message
        }, 201
        return response

class ResponseErrorBadRequest:

    def without_results(error, message):
        response = {
            "error_code": error,
            "message": message
        }, 422
        return response
    
    def with_results(error, message, details):
        response = {
            "error_code": error,
            "message": message,
            "details": details
        }, 422
        return response