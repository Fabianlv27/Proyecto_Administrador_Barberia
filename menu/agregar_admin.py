
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.sesion.hash_manager import HashManager


def agregar_admin():
    print("Función para agregar un nuevo administrador")
    contraseña = "admin123"
    contraseña_hasheada = HashManager.crear_hash(contraseña)
    
    JsonBasicCRUD("Data/index_correo.json").create("fabianlv1920@gmail .com", {"contraseña": contraseña_hasheada,"user_id": "95088210-9988-4682-965a-0635489f6645"})
    
    JsonBasicCRUD("Data/usuarios.json").create("95088210-9988-4682-965a-0635489f6645",{
    "nombre": "Fabian",
    "apellido": "Luna Vicente",
    "numero": "123456789",
    "correo": "fabianlv1920@gmail.com",
    "contraseña": contraseña_hasheada,
    "rol": ["admin_general", "admin_local", "empleado", "barbero"],
    "DNI": "00000000A",
    "estado": "Trabajando",
    "sueldo": 6000,
    "Ciudad": "Madrid",
    "Provincia": "Madrid",
    "codigo_postal": 28001,
    "direccion": "Sede Central 1",
    "dia_inicio": "2023-01-01",
    "informacion_adicional": "Fundador"
  } )
    print("Administrador agregado exitosamente")