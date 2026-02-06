from pydantic import ValidationError
from models.local import Local  
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, limpiar_pantalla, pausar
from menu.m_plantilla import menu_plantilla
from menu.menus_secundarios.admin_general.gestionar_reportes import GestorReportes

class GestorLocales:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/locales.json")
        self.reportes = GestorReportes() 

    def listar(self):
        limpiar_pantalla()
        print("--- 🏢 RED DE SUCURSALES (GLOBAL) ---")
        locales = self.db.read_all()
        
        if not locales:
            print("No hay locales registrados.")
        else:
            print(f"{'ID':<8} | {'NOMBRE':<25} | {'CIUDAD':<15} | {'ESTADO':<10}")
            print("-" * 65)
            for lid, d in locales.items():
                estado = "✅ Activo" if d.get('activo') else "❌ Cerrado"
                print(f"{lid:<8} | {d.get('nombre')[:25]:<25} | {d.get('ciudad')[:15]:<15} | {estado}")
        
        pausar()

    def inspeccionar_local(self):
        """Permite al Admin General entrar al dashboard de un local específico"""
        self.listar()
        lid = input("\n🔍 Ingrese el ID del local a inspeccionar (Enter para salir): ").strip().upper()
        if not lid: return

        local = self.db.read(lid)
        if not local:
            print("❌ Error: Local no encontrado.")
            pausar()
            return

        print(f"\nEntrando en modo inspección para: {local.get('nombre')}...")
        self.reportes.ver_dashboard(local_id_filtro=lid)

    def crear(self):
        limpiar_pantalla()
        print("--- ✨ INAUGURAR NUEVA SUCURSAL ---")
        
        try:
            raw_data = {
                "id_local": input_no_vacio("ID Local (ej. MAD01): ").upper(),
                "nombre": input_no_vacio("Nombre Comercial: "),
                "direccion": input_no_vacio("Dirección: "),
                "ciudad": input_no_vacio("Ciudad: "),
                "provincia": input("Provincia: ").strip() or "Madrid",
                "codigo_postal": int(input("Código Postal: ") or 28000),
                "telefono": input_no_vacio("Teléfono: "),
                "capacidad_barberos": int(input("Capacidad (sillas): ") or 3),
                "servicios_disponibles": ["Corte", "Barba", "Tinte"], # Default
                "horario_apertura": input("Apertura (HH:MM): ") or "09:00",
                "horario_cierre": input("Cierre (HH:MM): ") or "21:00",
                "activo": True
            }

            nuevo_local = Local(**raw_data)
            
            datos_dump = nuevo_local.model_dump()
            lid = datos_dump["id_local"] 
            
            if self.db.create(lid, datos_dump):
                print(f"\n✅ Local {nuevo_local.nombre} creado exitosamente.")
            else:
                print(f"\n❌ Error: El ID {lid} ya existe en la red.")

        except ValueError:
            print("\n❌ Error: Debes ingresar números válidos en CP o Capacidad.")
        except ValidationError as e:
            print("\n❌ Error de Validación de Datos:")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
        
        pausar()

    def cambiar_estado(self):
        self.listar()
        lid = input("\n🔄 ID del local a activar/desactivar: ").strip().upper()
        local = self.db.read(lid)
        
        if local:
            nuevo_estado = not local.get('activo', False)
            self.db.update(lid, {"activo": nuevo_estado})
            estado_str = "ABIERTO" if nuevo_estado else "CERRADO"
            print(f"\n✅ El local {lid} ahora está {estado_str}.")
        else:
            print("\n❌ Local no encontrado.")
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver Lista General", "funcion": self.listar},
            {"descripcion": "Inaugurar Nuevo Local", "funcion": self.crear},
            {"descripcion": "Activar/Desactivar Sede", "funcion": self.cambiar_estado},
            {"descripcion": "Inspeccionar Local (Dashboard)", "funcion": self.inspeccionar_local},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "GESTIÓN DE INMUEBLES")