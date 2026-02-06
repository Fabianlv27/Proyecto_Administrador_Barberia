from pydantic import ValidationError
from datetime import date
from models.ausencia import Ausencia
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorAusenciasLocal:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/ausencias.json")
        self.db_usuarios = JsonBasicCRUD("Data/usuarios.json")

    def _get_local(self):
        return get_sesion().get("local")

    def _es_empleado_mio(self, uid):
        """Verifica si un empleado pertenece al local de la sesión"""
        user = self.db_usuarios.read(uid)
        return user and user.get("local") == self._get_local()

    def listar_ausencias(self):
        limpiar_pantalla()
        lid = self._get_local()
        print(f"--- 🗓️ GESTIÓN DE AUSENCIAS ({lid}) ---")
        
        ausencias = self.db.read_all()
        encontradas = False
        
        print(f"{'EMPLEADO':<20} | {'TIPO':<15} | {'FECHAS':<25} | {'ESTADO'}")
        print("-" * 75)

        for aid, a in ausencias.items():
            uid_emp = a.get("id_empleado")
            
            # Filtro: Solo mostramos si el empleado es de MI local
            if self._es_empleado_mio(uid_emp):
                # Buscamos nombre para mostrarlo bonito
                emp_data = self.db_usuarios.read(uid_emp)
                nombre = emp_data.get("nombre", "Desconocido")
                
                fechas = f"{a['fecha_inicio']} -> {a['fecha_fin']}"
                estado = "✅ Aprobada" if a['aprobada'] else "⏳ Pendiente"
                
                print(f"{nombre[:20]:<20} | {a['tipo'][:15]:<15} | {fechas:<25} | {estado}")
                encontradas = True

        if not encontradas: print("No hay ausencias registradas.")
        pausar()

    def registrar_ausencia(self):
        limpiar_pantalla()
        print("--- ➕ REGISTRAR NUEVA AUSENCIA ---")
        
        # Pedimos ID de empleado
        uid_emp = input("ID del Empleado: ").strip()
        
        # Validación de seguridad
        if not self._es_empleado_mio(uid_emp):
            print("❌ Error: Ese empleado no pertenece a tu local o no existe.")
            pausar()
            return

        print("\nTipos: Vacaciones, Enfermedad, Asuntos Propios")
        try:
            raw_data = {
                "id_ausencia": generar_uuid(),
                "id_empleado": uid_emp,
                "tipo": input_no_vacio("Tipo de ausencia: "),
                "fecha_inicio": input_no_vacio("Fecha Inicio (YYYY-MM-DD): "),
                "fecha_fin": input_no_vacio("Fecha Fin (YYYY-MM-DD): "),
                "aprobada": True, # Si lo crea el admin local, nace aprobada
                "comentario": input("Comentario/Justificante: ")
            }

            # Validación Pydantic (valida formato de fechas automáticamente)
            nueva_ausencia = Ausencia(**raw_data)
            
            # Guardar
            datos = nueva_ausencia.model_dump()
            # Convertimos date a string para JSON
            datos["fecha_inicio"] = str(datos["fecha_inicio"])
            datos["fecha_fin"] = str(datos["fecha_fin"])
            
            self.db.create(datos["id_ausencia"], datos)
            print("✅ Ausencia registrada correctamente.")

        except ValidationError as e:
            print("\n❌ Error de Validación (Revisa el formato de fecha YYYY-MM-DD):")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
        except ValueError:
            print("❌ Error en datos.")
        
        pausar()

    def gestionar_estado(self):
        """Permite aprobar o cancelar una ausencia existente"""
        self.listar_ausencias()
        aid = input("\nID de la ausencia a modificar (Enter salir): ").strip()
        if not aid: return

        ausencia = self.db.read(aid)
        if ausencia and self._es_empleado_mio(ausencia["id_empleado"]):
            nuevo_estado = not ausencia["aprobada"]
            self.db.update(aid, {"aprobada": nuevo_estado})
            estado_str = "APROBADA" if nuevo_estado else "PENDIENTE/CANCELADA"
            print(f"✅ Estado cambiado a: {estado_str}")
        else:
            print("❌ Ausencia no encontrada o no tienes permisos.")
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver Calendario de Ausencias", "funcion": self.listar_ausencias},
            {"descripcion": "Registrar Baja/Vacaciones", "funcion": self.registrar_ausencia},
            {"descripcion": "Aprobar/Cancelar Solicitud", "funcion": self.gestionar_estado},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "RRHH - CONTROL DE AUSENCIAS")