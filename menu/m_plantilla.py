
def verificar_opcion(eleccion, tamaño):
    if eleccion.isdigit():
        eleccion = int(eleccion)
        return 1 <= eleccion <= tamaño
    return False

    
def menu_plantilla(opciones:list,titulo):
    
    print(titulo)
    for i,e in enumerate(opciones):
        print(f"{i+1}. {e['descripcion']}")
    eleccion = int(input("Seleccione una opción (1-{}): ".format(len(opciones))))
    while True:
        if not verificar_opcion(eleccion, len(opciones)):
            print("Opción no válida. Por favor, intente de nuevo.")
            eleccion = int(input("Seleccione una opción (1-{}): ".format(len(opciones))))
        else:
            break
    opciones[eleccion - 1]['funcion']()

   