import re
from funciones.general.crud_generico import JsonBasicCRUD

def validar_datos(correo, contraseña):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        return False, "Correo electrónico inválido"
    if len(contraseña) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    return True, None

def password_validator(correo, contraseña):
    user_data = JsonBasicCRUD("Data/index_correo.json").read(correo)
    if user_data is None:
        return False, "Correo no encontrado"
    if user_data.get("contraseña") != contraseña:
        return False, "Contraseña incorrecta"
    return True,user_data.get("user_id"), "Contraseña válida"

def pedir_datos_login():
    print("Por favor, ingresa tus datos de inicio de sesión:")
    correo = input("Correo electrónico: ")
    contraseña = input("Contraseña: ")
    return correo, contraseña

def menu_login():
    exito=False
    while True:
        print("=== Inicio de Sesión ===")
        correo, contraseña = pedir_datos_login()
        es_valido, mensaje_error = validar_datos(correo, contraseña)
        if es_valido:
            is_valid, user_id, message = password_validator(correo, contraseña)
            if not is_valid:
                print(message)
                continue
            JsonBasicCRUD("Data/sesion.json").create("sesion_actual", {"correo": correo, "contraseña": contraseña, "user_id": user_id})
            print("Inicio de sesión exitoso.")          
            exito=True
            break
        else:
            print(f"Error en el inicio de sesión: {mensaje_error}")
    if exito:
        #TO-DO: Llamar al menú principal de usuario
        return True