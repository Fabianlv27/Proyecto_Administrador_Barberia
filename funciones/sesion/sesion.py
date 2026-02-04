from funciones.general.crud_generico import JsonBasicCRUD


persona=None

def set_new_sesion(pers):
    global persona
    persona = pers
    JsonBasicCRUD("Data/sesion.json").update("sesion_actual", persona)
    
def set_sesion():
    global persona
    sesion_data = JsonBasicCRUD("Data/sesion.json").read("sesion_actual")
    persona_object = JsonBasicCRUD("Data/usuarios.json").read(sesion_data.get("user_id"))
    if persona_object is not None:
        persona = persona_object
        print(f"Sesión cargada para {persona.get('nombre')}")
    else:
        persona = None

def get_sesion():
    global persona
    return persona