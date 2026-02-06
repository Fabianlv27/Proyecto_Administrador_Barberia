from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar, input_no_vacio
from menu.m_plantilla import menu_plantilla

class GestorLocalesCliente:
    def __init__(self):
        self.db_locales = JsonBasicCRUD("Data/locales.json")
        self.db_usuarios = JsonBasicCRUD("Data/usuarios.json")
        self.db_reseñas = JsonBasicCRUD("Data/reseñas.json")

    def _calcular_puntuacion(self, target_id, tipo="local"):
        """Lógica exclusiva para calcular estrellas promedio"""
        reseñas = self.db_reseñas.read_all()
        total_puntos = 0
        contador = 0
        
        campo_busqueda = "id_local" if tipo == "local" else "id_barbero"
        
        # Si es local, hay que cruzar datos porque la reseña apunta a la cita, 
        # pero simplifiquemos: asumimos que buscamos reseñas directas o de barberos del local
        # Para este ejemplo, calculamos la media de los barberos del local
        
        if tipo == "barbero":
            for r in reseñas.values():
                if r.get("id_barbero") == target_id:
                    total_puntos += r.get("puntuacion", 0)
                    contador += 1
        
        return round(total_puntos / contador, 1) if contador > 0 else "N/A"

    def ver_catalogo_locales(self):
        limpiar_pantalla()
        print("--- 💈 DESCUBRE NUESTROS SALONES ---")
        locales = self.db_locales.read_all()
        usuarios = self.db_usuarios.read_all()
        
        # Filtramos solo locales activos
        activos = {k: v for k, v in locales.items() if v.get("activo") is True}
        
        for lid, l_data in activos.items():
            # Buscamos barberos de este local para calcular la media del local
            barberos_local = [uid for uid, u in usuarios.items() if u.get("local") == lid]
            puntuaciones = [self._calcular_puntuacion(bid, "barbero") for bid in barberos_local if isinstance(self._calcular_puntuacion(bid, "barbero"), float)]
            
            avg_local = sum(puntuaciones) / len(puntuaciones) if puntuaciones else 0
            estrellas = "⭐" * int(avg_local)
            
            print(f"\n📍 {l_data['nombre']} ({lid})")
            print(f"   Valoración: {avg_local}/5.0 {estrellas}")
            print(f"   Dirección:  {l_data['direccion']}, {l_data['ciudad']}")
            print(f"   Servicios:  {', '.join(l_data.get('servicios_disponibles', [])[:3])}...")
            print("-" * 40)
            
        lid = input("\nEscribe el ID del local para ver sus barberos (o Enter para salir): ").upper()
        if lid in activos:
            self._ver_barberos_de_local(lid)
        
    def _ver_barberos_de_local(self, lid):
        limpiar_pantalla()
        local = self.db_locales.read(lid)
        print(f"--- EQUIPO DE {local['nombre'].upper()} ---")
        
        usuarios = self.db_usuarios.read_all()
        encontrados = False
        
        for uid, u in usuarios.items():
            if u.get("local") == lid and "barbero" in u.get("rol", []):
                media = self._calcular_puntuacion(uid, "barbero")
                nombre = f"{u['nombre']} {u['apellido']}"
                print(f"✂️  {nombre:<25} | Puntuación: {media} ⭐")
                encontrados = True
                
        if not encontrados:
            print("No hay barberos disponibles en este local actualmente.")
        pausar()

    def menu_gestion(self):
        # Este menú es directo, no necesita subopciones complejas
        self.ver_catalogo_locales()