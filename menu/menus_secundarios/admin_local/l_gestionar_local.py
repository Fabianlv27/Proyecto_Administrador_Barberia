from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorMiLocal:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/locales.json")

    def _get_datos(self):
        lid = get_sesion().get("local")
        if not lid: return None, None
        return lid, self.db.read(lid)

    def ver_estado(self):
        limpiar_pantalla()
        lid, datos = self._get_datos()
        
        if not datos:
            print("❌ Error crítico: Local asignado no existe en BD.")
            pausar()
            return

        estado_icon = "🟢 ABIERTO" if datos.get("activo") else "🔴 CERRADO TEMPORALMENTE"
        
        print(f"=== 🏪 ADMINISTRACIÓN: {datos.get('nombre')} ===")
        print(f"📍 Dirección: {datos.get('direccion')}, {datos.get('ciudad')}")
        print(f"📞 Teléfono:  {datos.get('telefono')}")
        print(f"⏰ Horario:   {datos.get('horario_apertura')} - {datos.get('horario_cierre')}")
        print(f"Estado:       {estado_icon}")
        pausar()

    def editar_horario(self):
        limpiar_pantalla()
        lid, datos = self._get_datos()
        if not datos: return

        print(f"--- 🕒 EDITAR HORARIO ({lid}) ---")
        print(f"Actual: {datos.get('horario_apertura')} - {datos.get('horario_cierre')}")
        
        apertura = input("Nueva Apertura (HH:MM) [Enter para mantener]: ")
        cierre = input("Nuevo Cierre (HH:MM) [Enter para mantener]: ")
        
        update_data = {}
        if apertura: update_data["horario_apertura"] = apertura
        if cierre: update_data["horario_cierre"] = cierre
        
        if update_data:
            self.db.update(lid, update_data)
            print("✅ Horario actualizado.")
        else:
            print("No se hicieron cambios.")
        pausar()

    def editar_contacto(self):
        limpiar_pantalla()
        lid, datos = self._get_datos()
        if not datos: return

        print(f"--- 📞 EDITAR CONTACTO ---")
        nuevo_tel = input_no_vacio(f"Nuevo Teléfono (Actual: {datos.get('telefono')}): ")
        
        self.db.update(lid, {"telefono": nuevo_tel})
        print("✅ Teléfono actualizado.")
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver Estado del Local", "funcion": self.ver_estado},
            {"descripcion": "Modificar Horarios", "funcion": self.editar_horario},
            {"descripcion": "Modificar Teléfono", "funcion": self.editar_contacto},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "GESTIÓN DE SUCURSAL")