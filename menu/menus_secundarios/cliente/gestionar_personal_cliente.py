from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion

class GestorPersonalCliente:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")

    def _get_mi_id(self):
        return get_sesion().get("id")

    def ver_estadisticas(self):
        limpiar_pantalla()
        mi_id = self._get_mi_id()
        citas = [c for c in self.db_citas.read_all().values() if c.get("id_cliente") == mi_id]
        
        completadas = [c for c in citas if c.get("estado") == "Completada"]
        gasto_total = sum(c.get("precio", 0) for c in completadas)
        
        # Buscar barbero favorito
        conteo_barberos = {}
        for c in completadas:
            bid = c.get("id_barbero")
            conteo_barberos[bid] = conteo_barberos.get(bid, 0) + 1
            
        fav_id = max(conteo_barberos, key=conteo_barberos.get) if conteo_barberos else "Ninguno"

        print("--- 📊 MIS ESTADÍSTICAS ---")
        print(f"💰 Total Invertido: {gasto_total} €")
        print(f"✂️  Cortes realizados: {len(completadas)}")
        print(f"❤️ Barbero más visitado: {fav_id}")
        pausar()

    def ver_cupones(self):
        limpiar_pantalla()
        mi_id = self._get_mi_id()
        citas = [c for c in self.db_citas.read_all().values() if c.get("id_cliente") == mi_id and c.get("estado") == "Completada"]
        
        # Lógica simple de fidelidad: 1 cupón cada 5 citas
        total_citas = len(citas)
        cupones_ganados = total_citas // 5
        proximo_en = 5 - (total_citas % 5)
        
        print("--- 🎟️ MIS CUPONES ---")
        if cupones_ganados > 0:
            print(f"¡Tienes {cupones_ganados} cupón(es) de descuento del 50%!")
            for i in range(cupones_ganados):
                print(f"[{i+1}] CÓDIGO: FIDELIDAD-{mi_id[:4]}-{i}")
        else:
            print("Aún no tienes cupones disponibles.")
            
        print(f"\nTe faltan {proximo_en} cita(s) para tu próximo cupón.")
        print("[Barra de progreso]: " + "█" * (total_citas % 5) + "░" * proximo_en)
        pausar()