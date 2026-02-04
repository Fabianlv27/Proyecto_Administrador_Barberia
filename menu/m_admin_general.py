from menu.m_empleados import menu_empleados
from menu.m_admin_local import menu_admin_local
from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion

role_functions = {"admin_local": menu_admin_local, "empleado": menu_empleados}
persona=None

def manejo_roles(roles):
    new_options = []
    for rol in roles:
        if rol != "admin_general":
            new_options.append({"descripcion":"Menu "+rol,"funcion":role_functions.get(rol)})
    return new_options

def manejo_opciones():
    opciones = [{"descripcion": "Gestionar Todos los clientes", "funcion": None},
                {"descripcion": "Gestionar locales", "funcion": None},
                {"descripcion": "Gestionar Todos los empleados", "funcion": None},
                {"descripcion": "Ver Todos los reportes", "funcion": None},
                {"descripcion": "Configuración del sistema", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ]
    #Por si en un futuro se agregan más roles el admin general tambien puede ser empleado o admin local
    opciones.extend(manejo_roles(persona.get("rol", [])))   
    return opciones

def menu_admin_general():
    global persona
    persona=get_sesion()
    print(f"Bienvenido al menú de administrador general, {persona.get('nombre')}!")
    menu_plantilla(manejo_opciones(), "Menú Administrador General")
    return None