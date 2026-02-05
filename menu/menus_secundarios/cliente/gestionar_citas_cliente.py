from datetime import datetime
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorCitasCliente:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")
        self.db_locales = JsonBasicCRUD("Data/locales.json")
        self.db_usuarios = JsonBasicCRUD("Data/usuarios.json")

    def _get_mi_id(self):
        return get_sesion().get("id")

    def nueva_reserva(self):
        limpiar_pantalla()
        print("--- 📅 NUEVA RESERVA ---")
        
        # 1. Elegir Local
        lid = input_no_vacio("ID del Local preferido (ej. AAA88): ").upper()
        local = self.db_locales.read(lid)
        if not local: 
            print("Local no existe."); pausar(); return

        # 2. Elegir Barbero (Solo mostramos de ese local)
        print(f"\nBarberos disponibles en {local['nombre']}:")
        barberos = {k:v for k,v in self.db_usuarios.read_all().items() if v.get("local") == lid and "barbero" in v.get("rol",[])}
        for bid, bdata in barberos.items():
            print(f"- {bdata['nombre']} (ID: {bid})")
        
        bid = input_no_vacio("ID del Barbero: ")
        if bid not in barberos:
            print("Barbero inválido."); pausar(); return

        # 3. Datos de la cita
        servicio = input_no_vacio("Servicio (Corte/Barba/Tinte): ")
        fecha_str = input_no_vacio("Fecha y Hora (YYYY-MM-DDTHH:MM): ") # Formato ISO simplificado

        # Crear Cita
        cita_data = {
            "id_cita": generar_uuid(),
            "id_cliente": self._get_mi_id(),
            "id_barbero": bid,
            "id_local": lid,
            "fecha_hora": fecha_str, # Debería validarse fecha futura
            "servicio": servicio,
            "duracion_minutos": 30, # Default
            "precio": 15.0,        # Precio base hardcodeado para ejemplo
            "estado": "Pendiente",
            "notas_barbero": None
        }
        
        self.db_citas.create(cita_data["id_cita"], cita_data)
        print("\n✅ ¡Reserva confirmada! Te esperamos.")
        pausar()

    def ver_mis_citas(self):
        limpiar_pantalla()
        print("--- MIS CITAS ---")
        mi_id = self._get_mi_id()
        citas = self.db_citas.read_all()
        
        mis_citas = [c for c in citas.values() if c.get("id_cliente") == mi_id]
        
        if not mis_citas:
            print("No tienes historial de citas.")
        else:
            print(f"{'FECHA':<18} | {'SERVICIO':<15} | {'ESTADO'}")
            print("-" * 50)
            for c in mis_citas:
                print(f"{c['fecha_hora'][:16]:<18} | {c['servicio'][:15]:<15} | {c['estado']}")
        pausar()

    def cancelar_cita(self):
        self.ver_mis_citas()
        cid = input("\nID de la cita a cancelar (copiar del JSON o sistema): ") # En producción listarías el ID
        cita = self.db_citas.read(cid)
        
        if cita and cita["id_cliente"] == self._get_mi_id() and cita["estado"] == "Pendiente":
            self.db_citas.update(cid, {"estado": "Cancelada"})
            print("🚫 Cita cancelada.")
        else:
            print("No se puede cancelar (no existe o ya pasó).")
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Reservar nueva cita", "funcion": self.nueva_reserva},
            {"descripcion": "Ver historial/pendientes", "funcion": self.ver_mis_citas},
            {"descripcion": "Cancelar una cita", "funcion": self.cancelar_cita},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "GESTIÓN DE RESERVAS")