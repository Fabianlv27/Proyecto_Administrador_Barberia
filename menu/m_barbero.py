from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
from menu.menus_secundarios.barbero.gestion_reportes_barbero import GestorReportesBarbero
from menu.menus_secundarios.barbero.gestionar_citas_barbero import GestorCitasBarbero

persona=None

ctrl_agenda = GestorCitasBarbero()
ctrl_stats = GestorReportesBarbero()

def manejo_opciones():
    opciones = [{"descripcion": "Gestionar citas", "funcion": ctrl_agenda.menu_gestion},
                {"descripcion": "Ver estadisticas", "funcion": ctrl_stats.menu_gestion},
                {"descripcion": "(<-) volver", "funcion": None},
                ] 
    return opciones

def menu_barbero():
    global persona
    while True: 
        persona=get_sesion()
        print(f"Bienvenido al menú Barbero, {persona.get('nombre')}!")
        continuar=menu_plantilla(manejo_opciones(), "Menu Barbero")
        if not continuar:
            return