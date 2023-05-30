from enum import Enum

def validate_parameters(parametros, request):
    for parametro in parametros.keys():
        for validacion in parametros[parametro]:
            validacion.is_valid(argument=request.get(parametro), parameter=parametro)