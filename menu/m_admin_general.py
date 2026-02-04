from menu.m_empleados import menu_empleados
from menu.m_admin_local import menu_admin_local
from menu.m_plantilla import menu_plantilla

role_functions = {"admin_local": menu_admin_local, "empleado": menu_empleados}


def manejo_roles(roles):
    new_options = []
    for rol in roles:
        new_options.append({"descripcion":rol,"funcion":None})
    return new_options

def manejo_opciones(persona):
    opciones = [{"descripcion": "Gestionar Todos los clientes", "funcion": None},
                {"descripcion": "Gestionar locales", "funcion": None},
                {"descripcion": "Gestionar Todos los empleados", "funcion": None},
                {"descripcion": "Ver Todos los reportes", "funcion": None},
                {"descripcion": "Configuración del sistema", "funcion": None},
                {"descripcion": "Cerrar sesión", "funcion": None},
                ]
    #Por si en un futuro se agregan más roles el admin general tambien puede ser empleado o admin local
    opciones.extend(manejo_roles(persona.get("rol", [])))
    
    return opciones

def menu_admin_general(persona):
    print(f"Bienvenido al menú de administrador general, {persona.get('nombre')}!")
    menu_plantilla(manejo_opciones(persona), "Menú Administrador General")
    return None