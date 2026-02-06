import inquirer
from funciones.general.colores import Colores

from funciones.general.return_art import texto_a_ascii
from funciones.general.utils import limpiar_consola

def menu_plantilla(opciones:list, titulo):
    preguntas = [
        inquirer.List(
            'eleccion',
            message="",
            choices=[o["descripcion"] for o in opciones]
        )
    ]
    texto_a_ascii(titulo)
    respuesta = inquirer.prompt(preguntas)
    if respuesta is None:
        return False

    # Buscar el índice de la opción elegida
    idx = [o["descripcion"] for o in opciones].index(respuesta['eleccion'])
    funcion = opciones[idx]["funcion"]
    
    if funcion is not None:
        funcion()
        return True
    else:
        return False
