
from datetime import datetime, timedelta
from funciones.general.colores import Colores
from funciones.general.crud_generico import JsonBasicCRUD
from funciones.general.return_art import texto_a_ascii, texto_a_ascii_animado
from funciones.general.utils import input_no_vacio, generar_uuid, limpiar_pantalla, pausar
from funciones.sesion.sesion import get_sesion
from menu.m_plantilla import menu_plantilla

class GestorCitasCliente:
    def __init__(self):
        self.db_citas = JsonBasicCRUD("Data/citas.json")
        self.db_locales = JsonBasicCRUD("Data/locales.json")
        self.db_usuarios = JsonBasicCRUD("Data/usuarios.json")
        
        # Variables de estado para la reserva en curso
        self.local_id = None
        self.barbero_id = None
        self.fecha_seleccionada = None 
        self.hora_seleccionada = None

    def _get_mi_id(self):
        return get_sesion().get("user_id")
    
    # --- Setters para los menús (usados en lambdas) ---
    def select_local(self, id):
        self.local_id = id
        
    def select_barbero(self, id):
        self.barbero_id = id

    def select_fecha(self, fecha_obj):
        self.fecha_seleccionada = fecha_obj

    def select_hora(self, hora_str):
        self.hora_seleccionada = hora_str

    # --- LÓGICA DE CALENDARIO Y HORARIOS ---

    def _obtener_horario_barbero(self, barbero, local):
        """
        Devuelve objetos datetime con la hora de inicio y fin.
        Prioriza el horario del barbero; si no tiene, usa el del local.
        """
        fmt = "%H:%M"
        # Obtener strings de hora, con valores por defecto si faltan
        inicio_str = barbero.get("hora_inicio", local.get("horario_apertura", "09:00"))
        fin_str = barbero.get("hora_fin", local.get("horario_cierre", "20:00"))
        
        # Convertir a objetos datetime (la fecha será 1900-01-01, solo nos importa la hora)
        return datetime.strptime(inicio_str, fmt), datetime.strptime(fin_str, fmt)

    def _es_dia_laborable(self, fecha, barbero):
        """
        Verifica si la fecha cae en un día que el barbero trabaja.
        Usa el campo 'dias_semanas' (ej: 'LMXJV').
        """
        dias_str = barbero.get("dias_semanas", "LMXJVSD") # Default: trabaja todos los días
        
        # Mapa de Python (0=Lunes) a tus letras
        mapa_dias = {0: 'L', 1: 'M', 2: 'X', 3: 'J', 4: 'V', 5: 'S', 6: 'D'}
        
        dia_semana_num = fecha.weekday() # Obtiene 0, 1, 2...
        letra_dia = mapa_dias[dia_semana_num]
        
        return letra_dia in dias_str

    def _obtener_horas_ocupadas(self, barbero_id, fecha_str):
        """
        Busca en la BD todas las citas de ese barbero en esa fecha
        y devuelve una lista de horas (HH:MM) que ya están ocupadas.
        """
        ocupadas = []
        todas_citas = self.db_citas.read_all().values()
        
        for cita in todas_citas:
            # Filtros: Mismo barbero, misma fecha (ignorando hora), estado no cancelado
            if (cita.get("id_barbero") == barbero_id and 
                cita.get("fecha_hora", "").startswith(fecha_str) and 
                cita.get("estado") != "Cancelada"):
                
                # Extraer la hora "HH:MM" del ISO string "YYYY-MM-DDTHH:MM:SS"
                try:
                    hora_cita = cita["fecha_hora"].split("T")[1][:5]
                    ocupadas.append(hora_cita)
                except IndexError:
                    continue
        return ocupadas

    # --- FLUJO PRINCIPAL DE RESERVA ---

    def nueva_reserva(self):
        limpiar_pantalla()
        texto_a_ascii("NUEVA Cita", Colores.AZUL)
        
        # ---------------------------------------------------------
        # PASO 1: ELEGIR LOCAL
        # ---------------------------------------------------------
        opciones_locales = [
            {
                "descripcion": f"{l['nombre']}", 
                "funcion": lambda id_fijo=lid: self.select_local(id_fijo)
            } 
            for lid, l in self.db_locales.read_all().items() if l.get("activo")
        ]
        #opciones_locales.extend({"descripcion":"salir","funcion":None})
        
        # El menú devuelve el resultado de la lambda (None) o el valor seleccionado
        # Asumimos que menu_plantilla ejecuta la función. Verificamos self.local_id
        menu_plantilla(opciones_locales, "Elige locla")
        
        if not self.local_id:
            print("Operación cancelada en selección de local.")
            pausar()
            return

        local_data = self.db_locales.read(self.local_id)

        # ---------------------------------------------------------
        # PASO 2: ELEGIR BARBERO (Filtrado por local)
        # ---------------------------------------------------------
        barberos_dict = {
            k: v for k, v in self.db_usuarios.read_all().items() 
            if v.get("local") == self.local_id and "barbero" in v.get("rol", [])
        }

        if not barberos_dict:
            print(f"No hay barberos disponibles en {local_data['nombre']}.")
            pausar()
            return

        opciones_barberos = [
            {
                "descripcion": f"{b['nombre']} {b['apellido']} | Exp: {b.get('expriencia', 'N/A')}",
                "funcion": lambda id_fijo=bid: self.select_barbero(id_fijo)
            } 
            for bid, b in barberos_dict.items()
        ]

        menu_plantilla(opciones_barberos, f"Barberos")
        
        if not self.barbero_id:
            return # Cancelado o atrás

        barbero_data = barberos_dict[self.barbero_id]

        # ---------------------------------------------------------
        # PASO 3: ELEGIR FECHA (5 Días Disponibles)
        # ---------------------------------------------------------
        dias_disponibles = []
        fecha_iter = datetime.now().date() + timedelta(days=1) # Empezamos mañana
        
        # Buscamos los próximos 5 días que trabaje el barbero
        while len(dias_disponibles) < 5:
            if self._es_dia_laborable(fecha_iter, barbero_data):
                dias_disponibles.append(fecha_iter)
            fecha_iter += timedelta(days=1)

        opciones_dias = [
            {
                "descripcion": f"{dia.strftime('%A %d-%m-%Y')}", # Ej: Monday 12-02-2025
                "funcion": lambda d=dia: self.select_fecha(d)
            } for dia in dias_disponibles
        ]
        
        menu_plantilla(opciones_dias, f"Fechas de {barbero_data['nombre']}")
        
        if not self.fecha_seleccionada:
            return

        # ---------------------------------------------------------
        # PASO 4: ELEGIR HORA (Intervalos de 30 min)
        # ---------------------------------------------------------
        fecha_str_iso = self.fecha_seleccionada.strftime("%Y-%m-%d")
        
        # Obtener horas ya reservadas
        horas_ocupadas = self._obtener_horas_ocupadas(self.barbero_id, fecha_str_iso)
        
        # Calcular rango de trabajo
        h_inicio, h_fin = self._obtener_horario_barbero(barbero_data, local_data)
        
        horas_disponibles = []
        tiempo_actual = h_inicio
        
        # Generar bloques
        while tiempo_actual < h_fin:
            hora_str = tiempo_actual.strftime("%H:%M")
            
            # Solo agregar si NO está ocupada
            if hora_str not in horas_ocupadas:
                horas_disponibles.append(hora_str)
            
            tiempo_actual += timedelta(minutes=30) # Salto de 30 min

        if not horas_disponibles:
            print(Colores.ROJO + f"Lo siento, {barbero_data['nombre']} tiene la agenda llena para el {fecha_str_iso}." + Colores.RESET)
            pausar()
            return

        opciones_horas = [
            {
                "descripcion": f"{h} hs", 
                "funcion": lambda h_fija=h: self.select_hora(h_fija)
            } for h in horas_disponibles
        ]

        menu_plantilla(opciones_horas, f"Horas Disponibles")
        
        if not self.hora_seleccionada:
            return

        # ---------------------------------------------------------
        # PASO 5: CONFIRMAR Y GUARDAR
        # ---------------------------------------------------------
        fecha_final_iso = f"{fecha_str_iso}T{self.hora_seleccionada}:00"

        nuevo_id = generar_uuid()
        cita_data = {
            "id_cita": nuevo_id,
            "id_cliente": self._get_mi_id(),
            "id_barbero": self.barbero_id,
            "id_local": self.local_id,
            "fecha_hora": fecha_final_iso, 
            "servicio": "Corte de Cabello", # Podrías agregar un menú extra para servicios
            "duracion_minutos": 30, 
            "precio": 15.0,   
            "estado": "Pendiente",
            "notas_barbero": None
        }
        
        self.db_citas.create(nuevo_id, cita_data)
        
        print("\n" + "="*40)
        texto_a_ascii_animado("RESERVADO")
        print(f"Cita confirmada con {barbero_data['nombre']}")
        print(f"Fecha: {fecha_str_iso} a las {self.hora_seleccionada}")
        print("="*40)
        
        # Limpiar selección temporal
        self.local_id = None
        self.barbero_id = None
        self.fecha_seleccionada = None
        self.hora_seleccionada = None
        
        pausar()

    # --- OTRAS FUNCIONES ---

    def ver_mis_citas(self):
        limpiar_pantalla()
        print("--- MIS CITAS ---")
        mi_id = self._get_mi_id()
        citas = self.db_citas.read_all()
        
        mis_citas = [c for c in citas.values() if c.get("id_cliente") == mi_id]
        
        if not mis_citas:
            print("No tienes historial de citas.")
        else:
            print(f"{'FECHA':<20} | {'SERVICIO':<20} | {'ESTADO'}")
            print("-" * 60)
            for c in mis_citas:
                fecha_limpia = c['fecha_hora'].replace("T", " ")[:16]
                print(f"{fecha_limpia:<20} | {c.get('servicio', 'Varios')[:20]:<20} | {c['estado']}")
        pausar()

    def cancelar_cita(self):
        self.ver_mis_citas()
        print("\nPara cancelar, introduce el ID de la cita.")
        print("(Nota: En un sistema real seleccionarías de la lista anterior)")
        cid = input_no_vacio("ID de la cita: ") 
        
        cita = self.db_citas.read(cid)
        
        if cita and cita.get("id_cliente") == self._get_mi_id() and cita.get("estado") == "Pendiente":
            self.db_citas.update(cid, {"estado": "Cancelada"})
            print(Colores.VERDE + "\nCita cancelada correctamente." + Colores.RESET)
        else:
            print(Colores.ROJO + "\nNo se puede cancelar (ID incorrecto, no es tuya o ya pasó)." + Colores.RESET)
        pausar()

    def menu_gestion(self):
        while True:
            limpiar_pantalla()
            opciones = [
                {"descripcion": "Reservar nueva cita ($15)", "funcion": self.nueva_reserva},
                {"descripcion": "Ver mis citas", "funcion": self.ver_mis_citas},
                {"descripcion": "Cancelar una cita", "funcion": self.cancelar_cita},
                {"descripcion": "Volver", "funcion": None}
            ]
            
            seleccion = menu_plantilla(opciones, "GESTIon citas")
            if not seleccion:
                break

