from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar

class GestorReportes:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")
        self.db_usuarios = JsonBasicCRUD("Data/usuarios.json")
        self.db_locales = JsonBasicCRUD("Data/locales.json")

    def ver_dashboard(self, local_id_filtro=None):
        limpiar_pantalla()
        
        # Carga
        citas = self.db_citas.read_all()
        usuarios = self.db_usuarios.read_all()
        locales = self.db_locales.read_all()

        # Filtrado
        if local_id_filtro:
            titulo = f"SUCURSAL {local_id_filtro}"
            citas_fil = [c for c in citas.values() if c.get("id_local") == local_id_filtro]
            staff_fil = [u for u in usuarios.values() if u.get("local") == local_id_filtro and "cliente" not in u.get("rol", [])]
            n_locales = 1
        else:
            titulo = "HOLDING GLOBAL"
            citas_fil = list(citas.values())
            staff_fil = [u for u in usuarios.values() if "cliente" not in u.get("rol", [])]
            n_locales = len(locales)

        # Cálculos
        ingresos = sum(c.get("precio", 0) for c in citas_fil if c.get("estado") == "Completada")
        pendientes = sum(1 for c in citas_fil if c.get("estado") == "Pendiente")

        print(f"=== 📊 DASHBOARD: {titulo} ===")
        print(f"🏢 Locales:          {n_locales}")
        print(f"👥 Empleados:        {len(staff_fil)}")
        print(f"📅 Citas Totales:    {len(citas_fil)}")
        print(f"⏳ Pendientes:       {pendientes}")
        print("-" * 30)
        print(f"💰 FACTURACIÓN:      {ingresos:,.2f} €")
        
        pausar()

    def menu_gestion(self):
        self.ver_dashboard()