from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion

persona=None


def manejo_opciones():
    opciones = [{"descripcion": "Justificar una falta", "funcion": None},
                {"descripcion": "Ver informacion general", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ]
    
    return opciones

def menu_empleados():
    global persona
    while True:
        persona=get_sesion()
        print(f"___Menú de empleado!____")
        continuar=menu_plantilla(manejo_opciones(), "Menú Administrador Local")
        if not continuar:
            return