class ResponseOk:
    
    @classmethod
    def without_results(cls, code, message):
        response = {
            "code": code,
            "message": message
        }, 200
        return response
    
    @classmethod
    def with_results(cls, code, message, result):
        response = {
            "code": code,
            "message": message,
            "response": result
        }, 200
        return response

class CreatedOk:
    
    @classmethod
    def without_results(cls, code, message):
        response = {
            "code": code,
            "message": message
        }, 201
        return response

class ResponseErrorBadRequest:

    @classmethod
    def without_results(cls, error, message):
        response = {
            "error_code": error,
            "message": message
        }, 422
        return response
    
    @classmethod
    def with_results(cls, error, message, details):
        response = {
            "error_code": error,
            "message": message,
            "details": details
        }, 422
        return response