from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
from menu.menus_secundarios.admin_general.gestionar_clientes import GestorClientes
from menu.menus_secundarios.admin_general.gestionar_configuracion_sistema import GestorInfoGeneral
from menu.menus_secundarios.admin_general.gestionar_empleados import GestorEmpleados
from menu.menus_secundarios.admin_general.gestionar_locales import GestorLocales
from menu.menus_secundarios.admin_general.gestionar_reportes import GestorReportes
persona=None

ctrl_clientes = GestorClientes()
ctrl_empleados = GestorEmpleados()
ctrl_locales = GestorLocales()
ctrl_info = GestorInfoGeneral()
ctrl_reportes = GestorReportes()

def manejo_opciones():
    opciones = [
        {"descripcion": "Gestionar Todos los clientes", "funcion": ctrl_clientes.menu_gestion},
        {"descripcion": "Gestionar locales", "funcion": ctrl_locales.menu_gestion},
        {"descripcion": "Gestionar Todos los empleados", "funcion": ctrl_empleados.menu_gestion},
        {"descripcion": "Ver Dashboard y Reportes", "funcion": ctrl_reportes.menu_gestion},
        {"descripcion": "Configuración del sistema", "funcion": ctrl_info.menu_gestion},
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