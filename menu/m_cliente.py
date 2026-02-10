from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
from menu.menus_secundarios.cliente.gestionar_citas_cliente import GestorCitasCliente
from menu.menus_secundarios.cliente.gestionar_locales_cliente import GestorLocalesCliente
from menu.menus_secundarios.cliente.gestionar_personal_cliente import GestorPersonalCliente
from menu.menus_secundarios.cliente.gestionar_reseñas_cliente import GestorResenasCliente

persona=None
ctrl_citas = GestorCitasCliente()
ctrl_personal = GestorPersonalCliente()
ctrl_resenas = GestorResenasCliente()
ctrl_locales = GestorLocalesCliente()

def manejo_opciones():
    opciones = [{"descripcion": "Gestionar citas", "funcion": ctrl_citas.menu_gestion},
                {"descripcion": "Ver cupones", "funcion": ctrl_personal.ver_cupones},
                {"descripcion": "Dar reseña", "funcion": ctrl_resenas.menu_gestion},
                {"descripcion": "Ver estadisticas", "funcion": ctrl_personal.ver_estadisticas},
                {"descripcion":"Ver locales","funcion": ctrl_locales.menu_gestion},
                {"descripcion": "(<-) volver", "funcion": None}
                ] 
    return opciones

def menu_cliente():
    global persona
    while True:
        persona=get_sesion()
        print(f"Bienvenido al menú de cliente, {persona.get('nombre')}!")
        continuar=menu_plantilla(manejo_opciones(), "Menu Cliente")
        if not continuar:
            return