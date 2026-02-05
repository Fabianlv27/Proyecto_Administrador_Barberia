from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
persona=None

def manejo_opciones():
    opciones = [{"descripcion": "Gestionar Todos los clientes", "funcion": None},
                {"descripcion": "Gestionar locales", "funcion": None},
                {"descripcion": "Gestionar Todos los empleados", "funcion": None},
                {"descripcion": "Ver Todos los reportes", "funcion": None},
                {"descripcion": "Configuración del sistema", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ]
    return opciones

def menu_admin_general():
    global persona
    while True:
        persona=get_sesion()
        print(f"Bienvenido al menú de administrador general,    {persona.get('nombre')}!")
        continuar= menu_plantilla(manejo_opciones(), "Menú Administrador   General")
        if not continuar:
            return