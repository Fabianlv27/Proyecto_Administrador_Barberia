from funciones.general.crud_generico import JsonBasicCRUD


persona=None

def set_new_sesion(pers):
    global persona
    persona = pers
    JsonBasicCRUD("Data/sesion.json").update("sesion_actual", persona)
    
def set_sesion():
    global persona
    sesion_data = JsonBasicCRUD("Data/sesion.json").read("sesion_actual")
    if sesion_data is None:
        print("No hay sesión activa.")
        return None
    persona_object = JsonBasicCRUD("Data/usuarios.json").read(sesion_data.get("user_id"))
    if persona_object is not None:
        persona = persona_object
        persona["user_id"] = sesion_data.get("user_id")  
        print(f"Sesión cargada para {persona.get('nombre')}")
    else:
        persona = None

def cerrar_sesion():
    global persona
    persona = None
    JsonBasicCRUD("Data/sesion.json").delete("sesion_actual")
    print("Sesión cerrada.")

def get_sesion():
    global persona
    return persona