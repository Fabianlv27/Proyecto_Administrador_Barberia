from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.utils import limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
# Reutilizamos el gestor padre para no repetir código de crear/editar
from menu.menus_secundarios.admin_general.gestionar_clientes import GestorClientes

class GestorClientesLocal(GestorClientes):
    def __init__(self):
        super().__init__() # Inicializa self.db (usuarios)
        self.db_citas = JsonBasicCRUD("Data/citas.json")

    def listar(self):
        """Sobrescribe el listar global para filtrar por el local actual"""
        limpiar_pantalla()
        local_id = get_sesion().get("local")
        
        print(f"--- 👥 CLIENTES DE MI SUCURSAL ({local_id}) ---")
        
        # 1. Obtenemos IDs de clientes que han tenido citas en este local
        citas = self.db_citas.read_all()
        clientes_del_local = set()
        
        for c in citas.values():
            if c.get("id_local") == local_id:
                clientes_del_local.add(c.get("id_cliente"))
        
        # 2. Listamos cruzando datos
        usuarios = self.db.read_all()
        encontrados = False
        
        print(f"{'NOMBRE':<25} | {'TELÉFONO':<12} | {'ULT. CITA'}")
        print("-" * 60)
        
        for uid, d in usuarios.items():
            # Condición: Es cliente Y (tiene citas aquí O somos su favorito)
            es_cliente = "cliente" in d.get("rol", [])
            es_habitual = (uid in clientes_del_local) or (d.get("local_favorito") == local_id)
            
            if es_cliente and es_habitual:
                full_name = f"{d.get('nombre')} {d.get('apellido')}"
                print(f"{full_name:<25} | {d.get('numero'):<12} | {d.get('local_favorito', 'N/A')}")
                encontrados = True
        
        if not encontrados:
            print("No se encontraron clientes habituales en este local.")
            print("(Nota: Los clientes nuevos registrados aparecen tras su primera cita)")
        
        pausar()

    # NOTA: Hereda crear() y menu_gestion() del padre, 
    # pero usa el listar() nuevo automáticamente.