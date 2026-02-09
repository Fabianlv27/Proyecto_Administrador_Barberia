import shutil
import time
import unicodedata

from funciones.general.colores import Colores
from funciones.general.utils import limpiar_consola

ASCII_FONT = {
    "A": [
        "  ███  ",
        " █   █ ",
        " █████ ",
        " █   █ ",
        " █   █ "
    ],
    "B": [
        " ████  ",
        " █   █ ",
        " ████  ",
        " █   █ ",
        " ████  "
    ],
    "C": [
        "  ████ ",
        " █     ",
        " █     ",
        " █     ",
        "  ████ "
    ],
    "D": [
        " ████  ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " ████  "
    ],
    "E": [
        " █████ ",
        " █     ",
        " ████  ",
        " █     ",
        " █████ "
    ],
    "F": [
        " █████ ",
        " █     ",
        " ████  ",
        " █     ",
        " █     "
    ],
    "G": [
        "  ████ ",
        " █     ",
        " █  ██ ",
        " █   █ ",
        "  ████ "
    ],
    "H": [
        " █   █ ",
        " █   █ ",
        " █████ ",
        " █   █ ",
        " █   █ "
    ],
    "I": [
        " █████ ",
        "   █   ",
        "   █   ",
        "   █   ",
        " █████ "
    ],
    "J": [
        " █████ ",
        "    █  ",
        "    █  ",
        " █  █  ",
        "  ██   "
    ],
    "K": [
        " █   █ ",
        " █  █  ",
        " ███   ",
        " █  █  ",
        " █   █ "
    ],
    "L": [
        " █     ",
        " █     ",
        " █     ",
        " █     ",
        " █████ "
    ],
    "M": [
        " █   █ ",
        " ██ ██ ",
        " █ █ █ ",
        " █   █ ",
        " █   █ "
    ],
    "N": [
        " █   █ ",
        " ██  █ ",
        " █ █ █ ",
        " █  ██ ",
        " █   █ "
    ],
    "O": [
        "  ███  ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        "  ███  "
    ],
    "P": [
        " ████  ",
        " █   █ ",
        " ████  ",
        " █     ",
        " █     "
    ],
    "Q": [
        "  ███  ",
        " █   █ ",
        " █   █ ",
        " █  ██ ",
        "  ████ "
    ],
    "R": [
        " ████  ",
        " █   █ ",
        " ████  ",
        " █  █  ",
        " █   █ "
    ],
    "S": [
        "  ████ ",
        " █     ",
        "  ███  ",
        "     █ ",
        " ████  "
    ],
    "T": [
        " █████ ",
        "   █   ",
        "   █   ",
        "   █   ",
        "   █   "
    ],
    "U": [
        " █   █ ",
        " █   █ ",
        " █   █ ",
        " █   █ ",
        "  ███  "
    ],
    "V": [
        " █   █ ",
        " █   █ ",
        " █   █ ",
        "  █ █  ",
        "   █   "
    ],
    "W": [
        " █   █ ",
        " █   █ ",
        " █ █ █ ",
        " ██ ██ ",
        " █   █ "
    ],
    "X": [
        " █   █ ",
        "  █ █  ",
        "   █   ",
        "  █ █  ",
        " █   █ "
    ],
    "Y": [
        " █   █ ",
        "  █ █  ",
        "   █   ",
        "   █   ",
        "   █   "
    ],
    "Z": [
        " █████ ",
        "    █  ",
        "   █   ",
        "  █    ",
        " █████ "
    ],
    " ": [
        "       ",
        "       ",
        "       ",
        "       ",
        "       "
    ]
}



def limpiar_texto(texto):
    # normaliza caracteres Unicode
    texto = unicodedata.normalize("NFD", texto)
    # elimina tildes y diacríticos
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    # solo letras y espacios
    texto = "".join(c for c in texto if c.isalpha() or c == " ")
    return texto.upper()


def texto_a_ascii(texto,color=Colores.CIAN):
    texto = limpiar_texto(texto).upper() 

    lineas = [""] * 5  # altura de la fuente
    limpiar_consola()
    print(color)
    for letra in texto:
        if letra not in ASCII_FONT:
            raise ValueError(f"Caracter no soportado: {letra}")

        for i in range(5):
            lineas[i] += ASCII_FONT[letra][i] + "  "

    final= "\n".join(lineas)
    print(final)
    print(Colores.RESET)

def texto_a_ascii_animado(texto, delay=0.1):
    texto = limpiar_texto(texto)
    lineas = [""] * 5
    ancho_terminal = shutil.get_terminal_size().columns
    
    for letra in texto:
        if letra not in ASCII_FONT:
            raise ValueError(f"Caracter no soportado: {letra}")

        for i in range(5):
            lineas[i] += ASCII_FONT[letra][i] + "  "

        # limpiar pantalla
        print("\033c", end="")
        print(("\n")*5)
        # imprimir centrado
        for linea in lineas:
            print(linea.center(ancho_terminal))

        time.sleep(delay)
    time.sleep(1)  # pausa final para que se vea el mensaje completo
