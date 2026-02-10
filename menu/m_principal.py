from funciones.general.colores import Colores
from funciones.general.return_art import texto_a_ascii_animado
from funciones.sesion.sesion import get_sesion,set_sesion
from menu.m_barbero import menu_barbero
from menu.m_plantilla import menu_plantilla
from menu.m_login import menu_login
from menu.m_registro import menu_registro
from menu.m_admin_local import menu_admin_local
from menu.m_cliente import menu_cliente
from menu.m_admin_general import menu_admin_general
from menu.m_empleados import menu_empleados
from funciones.sesion.sesion import cerrar_sesion
from menu.menus_secundarios.m_informacion_general import GestorPerfil
persona =None
log_out = False
Perfil=GestorPerfil() # Instancia global del gestor de perfil
role_functions = {"empleado":menu_empleados,"admin_local":menu_admin_local,"admin_general":menu_admin_general,"cliente":menu_cliente,
                  "barbero":menu_barbero}

def accion_login():
    global log_out
    log_out=not menu_login()
    
def accion_registro():
    global log_out
    log_out=not menu_registro()

def accion_logout():
    global log_out
    texto_a_ascii_animado("Adios, " + persona.get("nombre", "Usuario") + "!")
    cerrar_sesion()
    log_out = True
    

def menu_no_login():
    opciones = [
        {"descripcion": "(¿Tienes cuenta?) Iniciar sesión", "funcion":accion_login},
        {"descripcion": "(¿Eres nuevo?) Registarse", "funcion": accion_registro},
        {"descripcion": "Salir", "funcion": None}]
    
    menu_plantilla(opciones, "Menú Principal")
    if not log_out:
        global persona
        set_sesion()
        persona = get_sesion()
        texto_a_ascii_animado("Hola, " + persona.get("nombre", "Usuario") + "!")
        return menu_with_login()
    return

def manejo_roles(roles):
    new_options = []
    for rol in roles:
        new_options.append({"descripcion":"Menu "+rol,"funcion":role_functions.get(rol)})
    return new_options


def menu_with_login():
    while True:
        opciones=[{"descripcion":"Informacion General","funcion":Perfil.menu_gestion}]
        
        opciones.extend(manejo_roles(persona.get("rol", [])))
        
        opciones.extend([{"descripcion": "Cerrar sesión",  "funcion":accion_logout},{"descripcion": "(<-) Salir", "funcion":     None}])  
        continuar= menu_plantilla(opciones, "Menú Principal")
        if not continuar:
            return
        if log_out:
            return menu_no_login()

def menu_principal():
    global persona
    set_sesion()
    persona = get_sesion()
    if persona is None:
        return menu_no_login()
    else:
        return menu_with_login()
