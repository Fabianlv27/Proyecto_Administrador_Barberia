from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from datetime import datetime

class GestorResenasCliente:
    def __init__(self):
        self.db_reseñas = JsonBasicCRUD("Data/reseñas.json")
        self.db_citas = JsonBasicCRUD("Data/citas.json")

    def _get_mi_id(self):
        return get_sesion().get("id")

    def escribir_reseña(self):
        limpiar_pantalla()
        mi_id = self._get_mi_id()
        
        # 1. Buscar citas completadas sin reseñar
        citas = self.db_citas.read_all()
        reseñas = self.db_reseñas.read_all()
        
        citas_reseñadas_ids = {r["id_cita"] for r in reseñas.values()}
        
        candidatas = []
        for cid, c in citas.items():
            if c["id_cliente"] == mi_id and c["estado"] == "Completada" and cid not in citas_reseñadas_ids:
                candidatas.append(c)
        
        if not candidatas:
            print("No tienes citas pendientes de valorar.")
            pausar()
            return

        print("--- ✍️ TU OPINIÓN IMPORTA ---")
        print("Citas disponibles para valorar:")
        for i, c in enumerate(candidatas):
            print(f"{i+1}. {c['fecha_hora']} - {c['servicio']}")
            
        try:
            sel = int(input("\nSelecciona el número: "))
            if 1 <= sel <= len(candidatas):
                cita_elegida = candidatas[sel-1]
                
                print(f"\nValorando: {cita_elegida['servicio']}")
                puntos = int(input("Puntuación (1-5): "))
                if not (1 <= puntos <= 5): raise ValueError
                
                comentario = input_no_vacio("Comentario: ")
                
                nueva_reseña = {
                    "id_reseña": generar_uuid(),
                    "id_cita": cita_elegida["id_cita"],
                    "id_cliente": mi_id,
                    "id_barbero": cita_elegida["id_barbero"],
                    "puntuacion": puntos,
                    "comentario": comentario,
                    "fecha": datetime.now().isoformat(),
                    "visible": True
                }
                
                self.db_reseñas.create(nueva_reseña["id_reseña"], nueva_reseña)
                print("✅ ¡Gracias por tu valoración!")
            else:
                print("Selección inválida.")
        except ValueError:
            print("Datos incorrectos.")
        
        pausar()

    def menu_gestion(self):
        # Directo a la función, sin submenú
        self.escribir_reseña()