from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion

class GestorReportesLocal:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")

    def ver_metricas(self):
        limpiar_pantalla()
        lid = get_sesion().get("local")
        if not lid: return

        citas_all = self.db_citas.read_all()
        
        # --- FILTRADO EN MEMORIA ---
        # Solo citas que coincidan con mi local_id
        citas_mias = [c for c in citas_all.values() if c.get("id_local") == lid]
        
        total = len(citas_mias)
        completadas = [c for c in citas_mias if c.get("estado") == "Completada"]
        pendientes = [c for c in citas_mias if c.get("estado") == "Pendiente"]
        canceladas = [c for c in citas_mias if c.get("estado") == "Cancelada"]
        
        ingresos = sum(c.get("precio", 0) for c in completadas)

        print(f"=== 📊 REPORTE DE RENDIMIENTO: {lid} ===")
        print(f"📅 Citas Totales:      {total}")
        print(f"✅ Completadas:        {len(completadas)}")
        print(f"⏳ Pendientes:         {len(pendientes)}")
        print(f"🚫 Canceladas:         {len(canceladas)}")
        print("-" * 30)
        print(f"💰 FACTURACIÓN TOTAL:  {ingresos:,.2f} €")
        
        if total > 0:
            tasa_cancelacion = (len(canceladas) / total) * 100
            print(f"📉 Tasa Cancelación:   {tasa_cancelacion:.1f}%")

        pausar()

    def menu_gestion(self):
        self.ver_metricas()