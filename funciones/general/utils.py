import uuid
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresione Enter para continuar...")

def generar_uuid():
    return str(uuid.uuid4())

def input_no_vacio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El campo no puede estar vacío.")

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')