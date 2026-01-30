import re
from funciones.general.crud_generico import JsonBasicCRUD

def validar_datos(correo, contraseña):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
        return False, "Correo electrónico inválido"
    if len(contraseña) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    return True, None

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
            JsonBasicCRUD("Data/sesion.json").create("sesion_actual", {"correo": correo, "contraseña": contraseña})
            print("Inicio de sesión exitoso.")          
            exito=True
            # Aquí iría la lógica para verificar las credenciales contra la base de datos
            break
        else:
            print(f"Error en el inicio de sesión: {mensaje_error}")
    if exito:
        #TO-DO: Llamar al menú principal de usuario
        return True