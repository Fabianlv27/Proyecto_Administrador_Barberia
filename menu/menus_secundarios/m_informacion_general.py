from funciones.general.utils import limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion

class GestorPerfil:
    def ver_perfil(self):
        limpiar_pantalla()
        u = get_sesion()
        if not u: return

        # --- DISEÑO VISUAL ---
        ancho = 50
        borde_h = "═" * ancho
        borde_v = "║"
        
        # Datos básicos formateados
        nombre_completo = f"{u.get('nombre', '')} {u.get('apellido', '')}"
        roles = ", ".join([r.upper() for r in u.get('rol', [])])
        
        print(f"╔{borde_h}╗")
        print(f"{borde_v} {'👤 MI PERFIL DE USUARIO':^{ancho-2}} {borde_v}")
        print(f"╠{borde_h}╣")
        
        # SECCIÓN 1: DATOS PERSONALES
        print(f"{borde_v} {'📋 DATOS PERSONALES':<{ancho-2}} {borde_v}")
        print(f"{borde_v} {'-' * (ancho-2):<{ancho-2}} {borde_v}")
        print(f"{borde_v} Nombre:   {nombre_completo[:35]:<37} {borde_v}")
        print(f"{borde_v} Email:    {u.get('correo', '')[:37]:<37} {borde_v}")
        print(f"{borde_v} Teléfono: {u.get('numero', '')[:37]:<37} {borde_v}")
        print(f"{borde_v} ID:       {u.get('id', '')[:37]:<37} {borde_v}")
        
        # SECCIÓN 2: DATOS DE CUENTA
        print(f"╠{borde_h}╣")
        print(f"{borde_v} {'🔐 SEGURIDAD':<{ancho-2}} {borde_v}")
        print(f"{borde_v} {'-' * (ancho-2):<{ancho-2}} {borde_v}")
        print(f"{borde_v} Roles:    {roles[:37]:<37} {borde_v}")
        print(f"{borde_v} Password: {'•' * 8:<37} {borde_v}")

        # SECCIÓN 3: DATOS ESPECÍFICOS (SEGÚN ROL)
        if "cliente" in u.get("rol", []):
            print(f"╠{borde_h}╣")
            print(f"{borde_v} {'❤️ FIDELIZACIÓN':<{ancho-2}} {borde_v}")
            print(f"{borde_v} {'-' * (ancho-2):<{ancho-2}} {borde_v}")
            fav = u.get('local_favorito', 'Sin asignar')
            print(f"{borde_v} Local Fav: {str(fav):<36} {borde_v}")
            print(f"{borde_v} Citas:     {str(u.get('n_citas', 0)):<36} {borde_v}")
        
        else: # Es empleado/barbero/admin
            print(f"╠{borde_h}╣")
            print(f"{borde_v} {'👔 DATOS LABORALES':<{ancho-2}} {borde_v}")
            print(f"{borde_v} {'-' * (ancho-2):<{ancho-2}} {borde_v}")
            
            local = u.get('local', 'N/A')
            if not local: local = "Oficina Central"
            
            sueldo = u.get('sueldo', 0)
            dias = u.get('dias_semanas', 'N/A')
            
            print(f"{borde_v} Sede:      {local:<36} {borde_v}")
            print(f"{borde_v} Jornada:   {dias:<36} {borde_v}")
            # Ocultamos sueldo a otros, pero uno mismo sí lo puede ver
            print(f"{borde_v} Salario:   {str(sueldo) + ' €':<36} {borde_v}")
            print(f"{borde_v} Estado:    {u.get('estado', 'Activo'):<36} {borde_v}")

        print(f"╚{borde_h}╝")
        
        pausar()
    
    def menu_gestion(self):
        # Como es solo ver, llamamos directo
        self.ver_perfil()