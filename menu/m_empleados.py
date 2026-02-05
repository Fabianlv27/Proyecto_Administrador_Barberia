from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
from menu.menus_secundarios.admin_general.gestionar_configuracion_sistema import GestorInfoGeneral
from menu.menus_secundarios.empleado.gestionar_ausencias_empleado import GestorAusenciasEmpleado

persona=None
ctrl_ausencias = GestorAusenciasEmpleado()
ctrl_info = GestorInfoGeneral()

def manejo_opciones():
    opciones = [{"descripcion": "Justificar una falta", "funcion": ctrl_ausencias.menu_gestion},
                {"descripcion": "Ver informacion general", "funcion": ctrl_info.ver_info},
                {"descripcion": "(<-) volver", "funcion": None},
                ]
    
    return opciones

def menu_empleados():
    global persona
    while True:
        persona=get_sesion()
        print(f"___Menú de empleado!____")
        continuar=menu_plantilla(manejo_opciones(), "")
        if not continuar:
            return