from menu.m_plantilla import menu_plantilla
from menu.m_login import menu_login
from menu.m_registro import menu_registro

def menu_principal():
    opciones = [
        {"descripcion": "(¿Tienes cuenta?) Iniciar sesión", "funcion": menu_login},
        {"descripcion": "(¿Eres nuevo?) Registarse", "funcion": menu_registro},
        {"descripcion": "Salir", "funcion": None}]
    
    menu_plantilla(opciones, "Menú Principal")