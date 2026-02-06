from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar, input_no_vacio
from menu.m_plantilla import menu_plantilla

class GestorInfoGeneral:
    def __init__(self):
        self.db = JsonBasicCRUD("Data/info_general.json")

    def ver_info(self):
        limpiar_pantalla()
        data = self.db.read_all()
        print("=== INFORMACIÓN DEL NEGOCIO (POO) ===\n")
        for seccion, contenido in data.items():
            print(f"--- {seccion.upper().replace('_', ' ')} ---")
            if isinstance(contenido, dict):
                for k, v in contenido.items():
                    print(f"  {k.capitalize()}: {v}")
            else:
                print(f"  {contenido}")
            print("")
        pausar()

    def _modificar_seccion(self, seccion):
        """Método privado auxiliar para editar una sección específica"""
        limpiar_pantalla()
        datos = self.db.read(seccion)
        if not datos: return

        print(f"--- EDITAR {seccion.upper()} ---")
        claves = list(datos.keys())
        for i, k in enumerate(claves):
            print(f"{i+1}. {k} (Actual: {datos[k]})")
        
        try:
            opc = int(input("\nElige campo a editar (0 salir): "))
            if opc == 0: return
            
            if 1 <= opc <= len(claves):
                campo = claves[opc-1]
                nuevo_valor = input_no_vacio(f"Nuevo valor para {campo}: ")
                
                # Intento de conversión simple
                if nuevo_valor.isdigit(): nuevo_valor = int(nuevo_valor)
                
                self.db.update(seccion, {campo: nuevo_valor})
                print("Guardado.")
        except ValueError:
            print("Entrada inválida.")
        pausar()

    # Wrappers para el menú
    def mod_basica(self): self._modificar_seccion("informacion_basica")
    def mod_contacto(self): self._modificar_seccion("contacto_central")
    def mod_params(self): self._modificar_seccion("parametros_sistema")

    def menu_gestion(self):
        opciones = [
            {"descripcion": "Ver Información Completa", "funcion": self.ver_info},
            {"descripcion": "Modificar Datos Básicos", "funcion": self.mod_basica},
            {"descripcion": "Modificar Contacto", "funcion": self.mod_contacto},
            {"descripcion": "Modificar Parámetros", "funcion": self.mod_params},
            {"descripcion": "Volver", "funcion": None}
        ]
        menu_plantilla(opciones, "CONFIGURACIÓN DEL SISTEMA")