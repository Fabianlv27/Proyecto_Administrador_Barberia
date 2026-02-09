from pydantic import ValidationError
from models.schemas import Empleado  # Tu modelo Pydantic
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from menu.m_plantilla import menu_plantilla

class GestorEmpleados:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/usuarios.json")
        # Cargamos locales para validar asignaciones al contratar
        self.db_locales = JsonBasicCRUD("Data/locales.json") 

    def listar(self, local_id_filtro=None):
        """
        Muestra empleados. 
        Si local_id_filtro es None -> Muestra TODOS.
        Si tiene valor -> Muestra solo los de ese local.
        """
        limpiar_pantalla()
        
        if local_id_filtro:
            print(f"--- 👥 PLANTILLA DEL LOCAL {local_id_filtro} ---")
        else:
            print("--- 👥 PLANTILLA GLOBAL (TODOS) ---")

        usuarios = self.db.read_all()
        encontrados = False
        
        # Cabecera
        print(f"{'ID':<8} | {'NOMBRE COMPLETO':<25} | {'ROL':<20} | {'LOCAL':<8}")
        print("-" * 70)

        for uid, d in usuarios.items():
            roles = d.get("rol", [])
            local_usuario = d.get("local", "N/A")

            # 1. Filtro de Rol: Excluir clientes puros
            es_staff = any(r in roles for r in ["empleado", "barbero", "admin_local", "admin_general"])
            
            # 2. Filtro de Local (Si aplica)
            cumple_filtro = (local_id_filtro is None) or (local_usuario == local_id_filtro)

            if es_staff and cumple_filtro:
                nombre_full = f"{d.get('nombre')} {d.get('apellido')}"
                roles_str = ",".join(roles)
                print(f"{uid} | {nombre_full[:25]:<25} | {roles_str[:20]:<20} | {local_usuario:<8}")
                encontrados = True
        
        if not encontrados:
            print("\nNo se encontraron empleados con estos criterios.")
        
        pausar()

    def contratar(self):
        limpiar_pantalla()
        print("--- 🤝 CONTRATAR EMPLEADO (GLOBAL) ---")
        
        # Input de roles
        print("Roles disponibles: empleado, barbero, admin_local")
        roles_raw = input("Ingrese roles (sep. coma): ").lower().replace(" ", "")
        lista_roles = roles_raw.split(",") if roles_raw else ["empleado"]

        try:
            # Recolección de datos
            # Nota: Al ser Admin General, asignamos el local manualmente
            raw_data = {
                "id": generar_uuid(),
                "nombre": input_no_vacio("Nombre: "),
                "apellido": input_no_vacio("Apellido: "),
                "numero": input_no_vacio("Teléfono: "),
                "correo": input_no_vacio("Correo: "),
                "contraseña": "temp123", # Pendiente: Hashear
                "rol": lista_roles,
                "sueldo": float(input("Sueldo mensual: ") or 0),
                "local": input("ID Local Asignado (ej. AAA88): ").strip().upper(),
                "estado": "Trabajando",
                "dias_semanas": input("Días laborales (ej LMXJV): ") or "LMXJV"
            }

            # Verificación de que el local existe antes de validar con Pydantic
            if not self.db_locales.read(raw_data["local"]):
                print(f"\n⚠️ Advertencia: El local {raw_data['local']} no existe en la base de datos.")
                if input("¿Continuar de todos modos? (s/n): ").lower() != 's':
                    return

            # Validación Pydantic
            nuevo_empleado = Empleado(**raw_data)
            
            # Guardado
            datos_dump = nuevo_empleado.model_dump()
            uid = datos_dump.pop("id")
            
            self.db.create(uid, datos_dump)
            print(f"\n✅ {nuevo_empleado.nombre} ha sido contratado/a correctamente.")

        except ValueError:
            print("\n❌ Error: El sueldo debe ser un número.")
        except ValidationError as e:
            print("\n❌ Error de Validación:")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
        
        pausar()

    def despedir(self):
        # Reutilizamos listar sin filtro para que vea a todos
        self.listar()
        uid = input("\n🚫 ID del empleado a dar de baja: ").strip()
        
        usuario = self.db.read(uid)
        
        if usuario:
            # Seguridad básica: no borrar clientes desde aquí
            if "cliente" in usuario.get("rol", []):
                print("❌ Error: Este ID pertenece a un CLIENTE. Usa el gestor de clientes.")
            else:
                confirm = input(f"¿Seguro que deseas despedir a {usuario.get('nombre')}? (s/n): ")
                if confirm.lower() == 's':
                    self.db.delete(uid)
                    print("✅ Empleado eliminado del sistema.")
        else:
            print("❌ Usuario no encontrado.")
        pausar()

    def menu_gestion(self):
        
        opciones = [
            {"descripcion": "Ver Plantilla Completa", "funcion": self.listar},
            {"descripcion": "Contratar Nuevo Empleado", "funcion": self.contratar},
            {"descripcion": "Despedir Empleado", "funcion": self.despedir},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "RECURSOS HUMANOS (RRHH)")