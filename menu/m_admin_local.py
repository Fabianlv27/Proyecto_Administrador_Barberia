from menu.m_plantilla import menu_plantilla
from funciones.sesion.sesion import get_sesion
from menu.menus_secundarios.admin_local.l_gestion_reportes import GestorReportesLocal
from menu.menus_secundarios.admin_local.l_gestionar_ausencias import GestorAusenciasLocal
from menu.menus_secundarios.admin_local.l_gestionar_clientes import GestorClientesLocal
from menu.menus_secundarios.admin_local.l_gestionar_empleados import GestorEmpleadosLocal
from menu.menus_secundarios.admin_local.l_gestionar_local import GestorMiLocal
persona=None

ctrl_clientes = GestorClientesLocal()  # Usamos la versión filtrada
ctrl_ausencias = GestorAusenciasLocal() # Usamoselnuevo gestor
ctrl_mi_local = GestorMiLocal()
ctrl_mis_empleados = GestorEmpleadosLocal()
ctrl_mis_reportes = GestorReportesLocal()

def manejo_opciones():
    opciones = [
        {"descripcion": "Gestionar mi Equipo (RRHH)", "funcion": ctrl_mis_empleados.menu_gestion},
        {"descripcion": "Control de Ausencias y Vacaciones", "funcion": ctrl_ausencias.menu_gestion}, 
        {"descripcion": "Administrar mi Local", "funcion": ctrl_mi_local.menu_gestion},
        {"descripcion": "Mis Clientes", "funcion": ctrl_clientes.menu_gestion},
        {"descripcion": "Ver Reportes", "funcion": ctrl_mis_reportes.menu_gestion},
                {"descripcion": "(<-) volver", "funcion": None},
                ]  
    return opciones

def menu_admin_local():
    global persona
    while True: 
        persona=get_sesion()
        print(f"Bienvenido al menú de administrador local, {persona.get('nombre')}!")
        continuar=menu_plantilla(manejo_opciones(), "Menú Administrador Local")
        if not continuar:
            return