from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar, input_no_vacio
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorCitasBarbero:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")
        self.db_usuarios = JsonBasicCRUD("Data/usuarios.json") # Para ver nombres de clientes

    def _get_mi_id(self):
        return get_sesion().get("id")

    def ver_agenda(self):
        limpiar_pantalla()
        mi_id = self._get_mi_id()
        print("--- ✂️ MI AGENDA DE CITAS ---")
        
        citas = self.db_citas.read_all()
        usuarios = self.db_usuarios.read_all()
        
        # Filtramos solo mis citas
        mis_citas = [c for c in citas.values() if c.get("id_barbero") == mi_id]
        
        # Ordenamos por fecha (string ISO permite ordenar alfabéticamente)
        mis_citas.sort(key=lambda x: x.get("fecha_hora", ""))

        print(f"{'ID':<6} | {'FECHA/HORA':<16} | {'CLIENTE':<20} | {'SERVICIO':<20} | {'ESTADO'}")
        print("-" * 85)
        
        encontradas = False
        for c in mis_citas:
            # Buscamos nombre del cliente
            cliente = usuarios.get(c.get("id_cliente"), {})
            nombre_cliente = f"{cliente.get('nombre', 'Desc.')} {cliente.get('apellido', '')}"
            
            # Formato fecha simple
            fecha_corta = c.get("fecha_hora", "")[:16].replace("T", " ")
            
            print(f"{c.get('id_cita'):<6} | {fecha_corta:<16} | {nombre_cliente[:20]:<20} | {c.get('servicio')[:20]:<20} | {c.get('estado')}")
            encontradas = True
            
        if not encontradas: print("No tienes citas asignadas.")
        pausar()

    def gestionar_cita(self):
        """Permite cambiar el estado de una cita o añadir notas"""
        self.ver_agenda() # Mostramos la lista primero
        
        cita_id = input("\nIngrese ID de la cita a gestionar (o Enter para salir): ").strip()
        if not cita_id: return
        
        cita = self.db_citas.read(cita_id)
        
        # Seguridad: Verificar que la cita es mía
        if not cita or cita.get("id_barbero") != self._get_mi_id():
            print("❌ Error: Cita no encontrada o no te pertenece.")
            pausar()
            return

        print(f"\nGestionando cita con cliente...")
        print("1. Marcar como COMPLETADA ✅")
        print("2. Marcar como CANCELADA ❌")
        print("3. Añadir Nota/Comentario 📝")
        print("0. Volver")
        
        opc = input("Seleccione acción: ")
        updates = {}
        
        if opc == "1":
            updates["estado"] = "Completada"
            print("✅ Cita finalizada.")
        elif opc == "2":
            updates["estado"] = "Cancelada"
            print("🚫 Cita cancelada.")
        elif opc == "3":
            nota = input_no_vacio("Escribe la nota (ej. 'Cliente sensible, usar navaja suave'): ")
            # Concatenamos si ya existía nota
            nota_actual = cita.get("notas_barbero")
            nuevo_texto = f"{nota_actual} | {nota}" if nota_actual else nota
            updates["notas_barbero"] = nuevo_texto
            print("📝 Nota guardada.")
        else:
            return

        if updates:
            self.db_citas.update(cita_id, updates)
        
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver Agenda Completa", "funcion": self.ver_agenda},
            {"descripcion": "Actualizar Estado de Cita", "funcion": self.gestionar_cita},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "AGENDA BARBERO")