from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion

persona=None

def manejo_opciones():
    opciones = [{"descripcion": "Gestionar citas", "funcion": None},
                {"descripcion": "Ver cupones", "funcion": None},
                {"descripcion": "Dar reseña", "funcion": None},
                {"descripcion": "Ver estadisticas", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ] 
    return opciones

def menu_cliente():
    global persona
    while True:
        persona=get_sesion()
        print(f"Bienvenido al menú de cliente, {persona.get('nombre')}!")
        continuar=menu_plantilla(manejo_opciones(persona), "Menú Administrador Local")
        if not continuar:
            return