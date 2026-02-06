from pydantic import ValidationError
from models.schemas import Empleado
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorEmpleadosLocal:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/usuarios.json")

    def _get_local_actual(self):
        """Obtiene el ID del local de la sesión actual de forma segura"""
        return get_sesion().get("local")

    def listar(self):
        limpiar_pantalla()
        lid = self._get_local_actual()
        if not lid:
            print("❌ Error: Tu usuario no tiene local asignado.")
            pausar()
            return

        print(f"--- 👥 MI EQUIPO (SUCURSAL {lid}) ---")
        usuarios = self.db.read_all()
        encontrados = False

        print(f"{'NOMBRE':<25} | {'ROL':<20} | {'ESTADO'}")
        print("-" * 60)
        
        for uid, d in usuarios.items():
            # FILTRO DE SEGURIDAD:
            # 1. Coincide el local
            # 2. No es un cliente
            if d.get("local") == lid and "cliente" not in d.get("rol", []):
                full_name = f"{d.get('nombre')} {d.get('apellido')}"
                roles = ",".join(d.get("rol", []))
                print(f"{full_name:<25} | {roles:<20} | {d.get('estado')}")
                encontrados = True
        
        if not encontrados: print("No tienes empleados asignados.")
        pausar()

    def contratar(self):
        limpiar_pantalla()
        lid = self._get_local_actual()
        if not lid: return

        print(f"--- 🤝 CONTRATAR PARA {lid} ---")
        
        # Solo permitimos roles básicos
        print("Roles disponibles: empleado, barbero")
        roles_input = input("Roles (sep. por coma): ").lower().split(",")
        # Limpiamos inputs
        roles_limpios = [r.strip() for r in roles_input if r.strip() in ["empleado", "barbero"]]
        
        if not roles_limpios: roles_limpios = ["empleado"]

        try:
            raw_data = {
                "id": generar_uuid(),
                "nombre": input_no_vacio("Nombre: "),
                "apellido": input_no_vacio("Apellido: "),
                "numero": input_no_vacio("Teléfono: "),
                "correo": input_no_vacio("Correo: "),
                "contraseña": "temp123", 
                "rol": roles_limpios,
                "sueldo": float(input("Sueldo mensual: ") or 0),
                "local": lid,  # <--- SE ASIGNA AUTOMÁTICAMENTE
                "estado": "Trabajando",
                "dias_semanas": input("Días (ej. LMXJV): ") or "LMXJV"
            }

            nuevo = Empleado(**raw_data)
            datos = nuevo.model_dump()
            uid = datos.pop("id")
            
            self.db.create(uid, datos)
            print(f"✅ {nuevo.nombre} se ha unido al equipo de {lid}.")

        except ValidationError as e:
            print("\n❌ Error de Validación:")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
        except ValueError:
            print("❌ Error: Datos numéricos inválidos.")
        
        pausar()

    def despedir(self):
        self.listar()
        lid = self._get_local_actual()
        
        nombre_buscar = input("\nIngrese el NOMBRE del empleado a despedir: ").lower()
        
        # Búsqueda por nombre (más amigable) dentro del local
        candidato_id = None
        candidato_data = None

        usuarios = self.db.read_all()
        for uid, d in usuarios.items():
            if d.get("local") == lid and nombre_buscar in d.get("nombre", "").lower():
                # Seguridad: no borrar clientes ni admins generales por error
                if "cliente" not in d.get("rol", []) and "admin_general" not in d.get("rol", []):
                    candidato_id = uid
                    candidato_data = d
                    break
        
        if candidato_id:
            confirm = input(f"¿Despedir a {candidato_data['nombre']} {candidato_data['apellido']}? (s/n): ")
            if confirm.lower() == 's':
                self.db.delete(candidato_id)
                print("✅ Baja tramitada correctamente.")
        else:
            print("❌ Empleado no encontrado en tu plantilla o no tienes permiso.")
        
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver mi Equipo", "funcion": self.listar},
            {"descripcion": "Contratar Personal", "funcion": self.contratar},
            {"descripcion": "Tramitar Baja (Despido)", "funcion": self.despedir},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "RRHH - SUCURSAL")