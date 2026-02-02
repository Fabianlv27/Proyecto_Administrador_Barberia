#Solo para Usuarios Nuevos , los empleados los mete el admin local o general
import re
import uuid

from funciones.general.crud_generico import JsonBasicCRUD

def validar_datos(nombre, apellido, numero, correo, contraseña):
    # Nombre
    if not nombre.strip() or len(nombre) < 2 or not nombre.replace(" ", "").isalpha():
        return False, "Nombre inválido"

    # Apellido
    if not apellido.strip() or len(apellido) < 2 or not apellido.replace(" ", "").isalpha():
        return False, "Apellido inválido"

    # Teléfono
    if not numero.isdigit() or not 8 <= len(numero) <= 15:
        return False, "Número de teléfono inválido"

    # Correo (opcional)
    if correo.strip():
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, correo):
            return False, "Correo electrónico inválido"

    # Contraseña
    if (
        len(contraseña) < 8 or
        not re.search(r"[A-Z]", contraseña) or
        not re.search(r"[a-z]", contraseña) or
        not re.search(r"\d", contraseña)
    ):
        return False, (
            "La contraseña debe tener al menos 8 caracteres, "
            "una mayúscula, una minúscula y un número"
        )

    return True, {
        "nombre": nombre.strip().title(),
        "apellido": apellido.strip().title(),
        "numero": numero,
        "correo": correo.strip() or None,
        "contraseña": contraseña
    }


def preguntar_datos_registro() -> dict:
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    numero = input("Ingrese su número de teléfono: ")
    correo = input("Ingrese su correo electrónico (opcional): ")
    contraseña = input("Cree una contraseña: ")
    return {
        "nombre": nombre,
        "apellido": apellido,
        "numero": numero,
        "correo": correo,
        "contraseña": contraseña
    }

def menu_registro():

    while True:
        print("=== Registro de Nuevo Usuario ===")
        datos = preguntar_datos_registro()
        es_valido, resultado = validar_datos(
            datos["nombre"],
            datos["apellido"],
            datos["numero"],
            datos["correo"],
            datos["contraseña"]
        )
        if es_valido:
            user_id = str(uuid.uuid4())
            JsonBasicCRUD("Data/index_correo.json").create(resultado["correo"], {"contraseña": resultado["contraseña"],"user_id": user_id})
            JsonBasicCRUD("Data/clientes.json").create(user_id, {
                "nombre": resultado["nombre"],
                "apellido": resultado["apellido"],
                "numero": resultado["numero"],
                "correo": resultado["correo"],
                "contraseña": resultado["contraseña"],
                "n_citas": 0,
                "total_gasto": 0,
                "citas": [],
                "local_favorito": None,
                "barbero_favorito": None
            })
            print("Registro exitoso. Datos validados:")
            for clave, valor in resultado.items():
                print(f"{clave.capitalize()}: {valor}")
            break
        else:
            print(f"Error de validación: {resultado}")
        repetir = input("¿Desea intentar registrarse de nuevo? (s/n): ").strip().lower()
        if repetir != 's':
            break