from menu.m_plantilla import menu_plantilla
from menu.m_login import menu_login
from menu.m_registro import menu_registro
from menu.m_admin_local import menu_admin_local
from menu.m_cliente import menu_cliente
from menu.m_admin_general import menu_admin_general
from menu.m_empleados import menu_empleados

def menu_no_login():
    opciones = [
        {"descripcion": "(¿Tienes cuenta?) Iniciar sesión", "funcion": menu_login},
        {"descripcion": "(¿Eres nuevo?) Registarse", "funcion": menu_registro},
        {"descripcion": "Salir", "funcion": None}]
    
    menu_plantilla(opciones, "Menú Principal")
    #big data,cloud ,IA,ciclo de vida de validacion ,prompt es una instruccion
    return None

def menu_with_login(persona):
    rol = persona["rol"]=list[str]
    if "general_admin" in rol:
        return menu_admin_general(persona)
    if "local_admin" in rol:  
        return menu_admin_local(persona)
    if 'cliente' in rol:
        return menu_cliente(persona)
    if "empleado" in rol:
        return menu_empleados(persona)
    return None

def menu_principal(persona=None):
    if persona is None:
        return menu_no_login()
    else:
        return menu_with_login(persona)
