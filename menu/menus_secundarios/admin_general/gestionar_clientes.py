from pydantic import ValidationError
from models.schemas import Cliente
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from menu.m_plantilla import menu_plantilla

class GestorClientes:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/usuarios.json")

    def listar(self):
        limpiar_pantalla()
        print("--- 👥 LISTA DE CLIENTES ---")
        usuarios = self.db.read_all()
        encontrados = False
        
        print(f"{'ID':<36} | {'NOMBRE':<20} | {'CORREO'}")
        print("-" * 80)
        
        for uid, d in usuarios.items():
            if "cliente" in d.get("rol", []):
                print(f"{uid:<36} | {d.get('nombre')} {d.get('apellido'):<15} | {d.get('correo')}")
                encontrados = True
        
        if not encontrados: print("No hay clientes registrados.")
        pausar()

    def crear(self):
        limpiar_pantalla()
        print("--- NUEVO CLIENTE ---")
        
        raw_data = {
            "id": generar_uuid(),
            "nombre": input_no_vacio("Nombre: "),
            "apellido": input_no_vacio("Apellido: "),
            "numero": input_no_vacio("Teléfono: "),
            "correo": input_no_vacio("Correo: "),
            "contraseña": "temp123", # Pendiente hashear
            "rol": ["cliente"],
            "citas": []
        }

        try:
            nuevo_cliente = Cliente(**raw_data)
            datos = nuevo_cliente.model_dump()
            uid = datos.pop("id")
            
            if self.db.create(uid, datos):
                print("✅ Cliente registrado exitosamente.")
            else:
                print("❌ Error: ID duplicado.")

        except ValidationError as e:
            print("\n❌ Error de Validación:")
            for error in e.errors():
                print(f"- {error['loc'][0]}: {error['msg']}")
        
        pausar()

    def eliminar(self):
        self.listar()
        uid = input("\n🗑️ ID del cliente a eliminar: ").strip()
        usuario = self.db.read(uid)
        
        if usuario and "cliente" in usuario.get("rol", []):
            if input(f"¿Eliminar a {usuario['nombre']}? (s/n): ") == 's':
                self.db.delete(uid)
                print("✅ Cliente eliminado.")
        else:
            print("❌ Cliente no encontrado.")
        pausar()

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver Lista de Clientes", "funcion": self.listar},
            {"descripcion": "Registrar Nuevo Cliente", "funcion": self.crear},
            {"descripcion": "Eliminar Cliente", "funcion": self.eliminar},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "GESTIÓN DE CLIENTES")