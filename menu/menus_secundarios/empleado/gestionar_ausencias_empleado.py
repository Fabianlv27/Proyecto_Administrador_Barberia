from pydantic import ValidationError
from models.ausencia import Ausencia
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorAusenciasEmpleado:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/ausencias.json")

    def _get_mi_id(self):
        return get_sesion().get("user_id")

    def ver_mis_solicitudes(self):
        limpiar_pantalla()
        uid = self._get_mi_id()
        print("--- 🗓️ MIS SOLICITUDES DE AUSENCIA ---")
        
        ausencias = self.db.read_all()
        encontradas = False
        
        print(f"{'FECHAS':<25} | {'TIPO':<15} | {'ESTADO'}")
        print("-" * 60)

        for aid, a in ausencias.items():
            if a.get("id_empleado") == uid:
                fechas = f"{a['fecha_inicio']} -> {a['fecha_fin']}"
                estado = "✅ Aprobada" if a['aprobada'] else "⏳ Pendiente/Revisión"
                print(f"{fechas:<25} | {a['tipo'][:15]:<15} | {estado}")
                encontradas = True

        if not encontradas: print("No tienes solicitudes registradas.")
        pausar()

    def justificar_falta(self):
        limpiar_pantalla()
        print("--- 📝 JUSTIFICAR FALTA / SOLICITAR DÍA ---")
        
        uid = self._get_mi_id()
        
        print("Tipos comunes: Enfermedad, Asuntos Propios, Vacaciones")
        try:
            raw_data = {
                "id_ausencia": generar_uuid(),
                "id_empleado": uid,
                "tipo": input_no_vacio("Motivo/Tipo: "),
                "fecha_inicio": input_no_vacio("Desde (YYYY-MM-DD): "),
                "fecha_fin": input_no_vacio("Hasta (YYYY-MM-DD): "),
                "aprobada": False, 
                "comentario": input("Detalles adicionales: ")
            }

            # Validación Pydantic
            nueva_solicitud = Ausencia(**raw_data)
            
            # Guardado
            datos = nueva_solicitud.model_dump()
            datos["fecha_inicio"] = str(datos["fecha_inicio"])
            datos["fecha_fin"] = str(datos["fecha_fin"])
            
            self.db.create(datos["id_ausencia"], datos)
            print("\n✅ Solicitud enviada al Administrador Local.")

        except ValidationError as e:
            print("\n❌ Error (Revisa formato de fechas YYYY-MM-DD):")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
        
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver historial de solicitudes", "funcion": self.ver_mis_solicitudes},
            {"descripcion": "Nueva solicitud / Justificar", "funcion": self.justificar_falta},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "GESTIÓN DE AUSENCIAS")