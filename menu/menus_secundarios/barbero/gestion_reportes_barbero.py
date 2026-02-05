from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion

class GestorReportesBarbero:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")
        self.db_reseñas = JsonBasicCRUD("Data/reseñas.json")

    def ver_mis_estadisticas(self):
        limpiar_pantalla()
        mi_id = get_sesion().get("id")
        
        citas = self.db_citas.read_all()
        reseñas = self.db_reseñas.read_all()
        
        # Filtros en memoria
        mis_citas = [c for c in citas.values() if c.get("id_barbero") == mi_id]
        mis_reseñas = [r for r in reseñas.values() if r.get("id_barbero") == mi_id]
        
        # Cálculos
        total_servicios = len(mis_citas)
        completados = [c for c in mis_citas if c.get("estado") == "Completada"]
        pendientes = [c for c in mis_citas if c.get("estado") == "Pendiente"]
        
        ingresos_generados = sum(c.get("precio", 0) for c in completados)
        
        # Cálculo de estrellas promedio
        promedio_estrellas = 0
        if mis_reseñas:
            suma_puntos = sum(r.get("puntuacion", 0) for r in mis_reseñas)
            promedio_estrellas = suma_puntos / len(mis_reseñas)

        print(f"=== 📊 MIS ESTADÍSTICAS DE RENDIMIENTO ===")
        print(f"✂️  Servicios Realizados: {len(completados)}")
        print(f"📅 Citas Pendientes:     {len(pendientes)}")
        print(f"💰 Total Generado:       {ingresos_generados:,.2f} €")
        print("-" * 35)
        print(f"⭐ Valoración Media:     {promedio_estrellas:.1f}/5.0 ({len(mis_reseñas)} reseñas)")
        
        pausar()

    def menu_gestion(self):
        # Directo a la visualización
        self.ver_mis_estadisticas()