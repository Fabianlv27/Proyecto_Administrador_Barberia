from menu.m_plantilla import menu_plantilla

def manejo_roles(roles):
    new_options = []
    for rol in roles[1:]:
        new_options.append({"descripcion":rol,"funcion":None})
    return new_options

def manejo_opciones(persona):
    opciones = [{"descripcion": "Gestionar clientes", "funcion": None},
                {"descripcion": "Gestionar locales", "funcion": None},
                {"descripcion": "Gestionar empleados", "funcion": None},
                {"descripcion": "Ver reportes", "funcion": None},
                {"descripcion": "Cerrar sesión", "funcion": None},
                ]
    #Por si en un futuro se agregan más roles el admin general tambien puede ser empleado o admin local
    opciones.extend(manejo_roles(persona.get("rol", [])))
    return opciones

def menu_admin_local(persona):
    print(f"Bienvenido al menú de administrador local, {persona.get('nombre')}!")
    menu_plantilla(manejo_opciones(persona), "Menú Administrador Local")
    return None