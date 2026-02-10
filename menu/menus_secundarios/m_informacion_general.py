from funciones.general.colores import Colores
from funciones.general.return_art import texto_a_ascii
from funciones.general.utils import limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion

class GestorPerfil:
    def ver_perfil(self):
        limpiar_pantalla()
        u = get_sesion()
        if not u: return

        # --- CONFIGURACIÓN DEL DISEÑO ---
        ancho_total = 60  # Ancho total del cuadro (ajústalo si quieres más/menos)
        ancho_etiqueta = 12 # Espacio reservado para "Nombre:", "Email:", etc.
        
        # Calculamos el espacio útil para el texto (Ancho total - bordes - espacios internos)
        # Borde izq(1) + espacio(1) + etiqueta + espacio(1) + valor + espacio(1) + Borde der(1)
        ancho_valor = ancho_total - 2 - 1 - ancho_etiqueta - 1 - 1 

        borde_h = "═" * (ancho_total - 2)
        borde_v = "║"
        sep_int = "-" * (ancho_total - 4)

        # --- FUNCIÓN AUXILIAR DE IMPRESIÓN ---
        def imprimir_linea(etiqueta, valor):
            # 1. Asegurar que el valor es string y no None
            val_str = str(valor) if valor is not None else ""
            
            # 2. CORTAR EL DATO (Truncar): Si es más largo que el hueco, se corta.
            # Esto evita que el borde derecho se desplace.
            if len(val_str) > ancho_valor:
                val_str = val_str[:ancho_valor-3] + "..." # Cortamos y añadimos puntos
            
            # 3. Formatear la línea
            # {Etiqueta alineada izq} {Valor alineado izq rellenado con espacios}
            contenido = f" {etiqueta:<{ancho_etiqueta}} {val_str:<{ancho_valor}} "
            print(f"{borde_v}{contenido}{borde_v}")

        def imprimir_titulo(texto):
            print(f"{borde_v} {texto:<{ancho_total-4}}{borde_v}")
            print(f"{borde_v} {sep_int} {borde_v}")

        # --- PREPARACIÓN DE DATOS ---
        nombre_completo = f"{u.get('nombre', '')} {u.get('apellido', '')}"
        roles = ", ".join([r.upper() for r in u.get('rol', [])])
        
        # ASCII Art (Nombre)
        texto_a_ascii(u.get('nombre',''), Colores.VERDE)

        # --- PINTAR EL CUADRO ---
        print(f"╔{borde_h}╗")
        # Centramos el título principal restando los bordes
        print(f"{borde_v}{'👤MI PERFIL DE USUARIO'.center(ancho_total-3)}{borde_v}")
        print(f"╠{borde_h}╣")
        
        # SECCIÓN 1: DATOS PERSONALES
        imprimir_titulo("📋 DATOS PERSONALES")
        imprimir_linea("Nombre:", nombre_completo)
        imprimir_linea("Email:", u.get('correo', ''))
        imprimir_linea("Teléfono:", u.get('numero', ''))
        imprimir_linea("ID:", u.get('id', ''))
        
        # SECCIÓN 2: DATOS DE CUENTA
        print(f"╠{borde_h}╣")
        imprimir_titulo("🔐 SEGURIDAD")
        imprimir_linea("Roles:", roles)
        imprimir_linea("Password:", "•" * 8)

        # SECCIÓN 3: DATOS ESPECÍFICOS
        if "cliente" in u.get("rol", []):
            print(f"╠{borde_h}╣")
            imprimir_titulo("❤️  FIDELIZACIÓN")
            fav = u.get('local_favorito', 'Sin asignar')
            imprimir_linea("Local Fav:", fav)
            imprimir_linea("Citas:", u.get('n_citas', 0))
        
        else: # Es empleado/barbero/admin
            print(f"╠{borde_h}╣")
            imprimir_titulo("👔 DATOS LABORALES")
            
            local = u.get('local', 'N/A')
            if not local: local = "Oficina Central"
            
            sueldo = u.get('sueldo', 0)
            dias = u.get('dias_semanas', 'N/A')
            
            imprimir_linea("Sede:", local)
            imprimir_linea("Jornada:", dias)
            # Convertimos sueldo a string con símbolo
            imprimir_linea("Salario:", f"{sueldo} €")
            imprimir_linea("Estado:", u.get('estado', 'Activo'))

        print(f"╚{borde_h}╝")
        
        pausar()

    def menu_gestion(self):
        self.ver_perfil()