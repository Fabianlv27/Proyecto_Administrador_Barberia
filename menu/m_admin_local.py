from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
persona=None


def manejo_opciones():
    opciones = [{"descripcion": "Gestionar clientes", "funcion": None},
                {"descripcion": "Gestionar locales", "funcion": None},
                {"descripcion": "Gestionar empleados", "funcion": None},
                {"descripcion": "Ver reportes", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ]  
    return opciones

def menu_admin_local():
    global persona
    while True: 
        persona=get_sesion()
        print(f"Bienvenido al menú de administrador local, {persona.get('nombre')}!")
        continuar=menu_plantilla(manejo_opciones(), "Menú Administrador Local")
        if not continuar:
            return