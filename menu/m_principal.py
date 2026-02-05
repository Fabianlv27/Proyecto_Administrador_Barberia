from funciones.sesion.sesion import get_sesion,set_sesion
from menu.m_barbero import menu_barbero
from menu.m_plantilla import menu_plantilla
from menu.m_login import menu_login
from menu.m_registro import menu_registro
from menu.m_admin_local import menu_admin_local
from menu.m_cliente import menu_cliente
from menu.m_admin_general import menu_admin_general
from menu.m_empleados import menu_empleados

persona =None

role_functions = {"empleado":menu_empleados,"admin_local":menu_admin_local,"admin_general":menu_admin_general,"cliente":menu_cliente,
                  "barbero":menu_barbero}


def menu_no_login():
    opciones = [
        {"descripcion": "(¿Tienes cuenta?) Iniciar sesión", "funcion": menu_login},
        {"descripcion": "(¿Eres nuevo?) Registarse", "funcion": menu_registro},
        {"descripcion": "Salir", "funcion": None}]
    
    menu_plantilla(opciones, "Menú Principal")
    return 

def manejo_roles(roles):
    new_options = []
    for rol in roles:
        new_options.append({"descripcion":"Menu "+rol,"funcion":role_functions.get(rol)})
    return new_options

def menu_with_login():
    while True:
        opciones = manejo_roles(persona.get("rol", []))
        print(persona)
        opciones.extend([{"descripcion": "(<-) Cerrar sesión",  "funcion": None},{"descripcion": "Salir", "funcion":     None}])  
        continuar= menu_plantilla(opciones, "Menú Principal")
        if not continuar:
            return

def menu_principal():
    global persona
    set_sesion()
    persona = get_sesion()
    if persona is None:
        return menu_no_login()
    else:
        return menu_with_login()
