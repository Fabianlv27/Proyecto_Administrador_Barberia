import re
from funciones.general.colores import Colores
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.return_art import texto_a_ascii
from funciones.sesion.hash_manager import HashManager
from funciones.sesion.sesion import set_sesion,set_new_sesion

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
    if not HashManager.verificar_hash(contraseña, user_data.get("contraseña")):
        return False, "Contraseña incorrecta"
    return True,user_data.get("user_id"), "Contraseña válida"

def pedir_datos_login():
    print("Por favor, ingresa tus datos de inicio de sesión:")
    correo = input("Correo electrónico: ")
    contraseña = input("Contraseña: ")
    return correo, contraseña

def set_complete_sesion(user_id):
    user_data = JsonBasicCRUD("Data/usuarios.json").read(user_id)
    set_new_sesion(user_data)

def menu_login():
    exito=False
    while True:
        texto_a_ascii("Login",Colores.VERDE)
        correo, contraseña = pedir_datos_login()
        es_valido, mensaje_error = validar_datos(correo, contraseña)
        if es_valido:
            is_valid, user_id, message = password_validator(correo, contraseña)
            if not is_valid:
                print(message)
                continue          
            JsonBasicCRUD("Data/sesion.json").create("sesion_actual", {"correo": correo, "contraseña": contraseña, "user_id": user_id})
            set_complete_sesion(user_id)
            print("Inicio de sesión exitoso.")          
            exito=True
            break
        else:
            print(f"Error en el inicio de sesión: {mensaje_error}")
    if exito:
        return True