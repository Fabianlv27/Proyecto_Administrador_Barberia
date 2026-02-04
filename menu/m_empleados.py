from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
from menu.m_barbero import menu_barbero

role_functions = {"barbero":menu_barbero}
persona=None

def manejo_roles(roles):
    new_options = []
    for rol in roles:
        if rol =="barbero":
            new_options.append({"descripcion":"Menu "+ rol,"funcion":role_functions.get(rol)})
    return new_options

def manejo_opciones():
    opciones = [{"descripcion": "Justificar una falta", "funcion": None},
                {"descripcion": "Ver informacion general", "funcion": None},
                {"descripcion": "(<-) volver", "funcion": None},
                ]
    #Por si en un futuro se agregan más roles el admin general tambien puede ser empleado o admin local
    opciones.extend(manejo_roles(persona.get("rol", [])))
    
    return opciones

def menu_empleados():
    global persona
    persona=get_sesion()
    print(f"___Menú de empleado!____")
    menu_plantilla(manejo_opciones(), "Menú Administrador Local")
    return None