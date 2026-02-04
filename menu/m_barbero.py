from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion

persona=None


def manejo_opciones():
    opciones = [{"descripcion": "Gestionar citas", "funcion": None},
                {"descripcion": "Ver estadisticas", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ]
    #Por si en un futuro se agregan más roles el admin general tambien puede ser empleado o admin local    
    return opciones

def menu_barbero():
    global persona
    persona=get_sesion()
    print(f"Bienvenido al menú Barbero, {persona.get('nombre')}!")
    menu_plantilla(manejo_opciones(), "Menú Administrador Local")
    return None