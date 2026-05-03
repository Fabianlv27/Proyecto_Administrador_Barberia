
# 💈 BarberERP - Sistema de Gestión Integral para Barberías (Prototipo)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pydantic](https://img.shields.io/badge/Pydantic-Data_Validation-e92063.svg)
![Estado](https://img.shields.io/badge/Estado-Prototipo_Académico-orange.svg)

Este proyecto es un prototipo funcional desarrollado como trabajo de grado. Simula la administración centralizada de una cadena de barberías (arquitectura multi-sucursal). Aunque actualmente opera bajo una interfaz de línea de comandos (CLI) y persistencia en archivos JSON, su lógica de negocio, validación de datos y separación de roles están conceptualizados para evolucionar hacia un **ERP (Enterprise Resource Planning)** completo.

## 🚀 Características Principales (Gestión por Roles)

El sistema cuenta con un control de acceso basado en roles (RBAC), limitando o habilitando funciones según el usuario autenticado:

### 👑 Administrador General (Sede Central)
- **Gestión Global:** Creación y supervisión de todas las sucursales (locales).
- **Recursos Humanos:** Contratación, despido y asignación de empleados/barberos a diferentes locales.
- **Auditoría y Reportes:** Acceso a un *Dashboard* global de facturación, volumen de citas y rendimiento métrico del negocio.
- **Configuración del Sistema:** Modificación de parámetros globales (políticas de cancelación, precios base, información corporativa).

### 🏪 Administrador Local (Gerente de Sucursal)
- **Control de la Sucursal:** Edición de horarios de apertura/cierre y datos de contacto de su propio local.
- **Gestión de Personal:** Administración exclusiva del equipo asignado a su local.
- **Control de Ausencias:** Aprobación o denegación de vacaciones, bajas por enfermedad o asuntos propios de sus empleados.
- **Analítica Local:** Visualización de la tasa de cancelación, ingresos y citas exclusivas de su sede.

### ✂️ Barbero / Empleado
- **Agenda Interactiva:** Visualización de citas programadas en tiempo real.
- **Ejecución de Citas:** Capacidad para marcar citas como completadas/canceladas y añadir notas sobre los clientes (ej. "Cliente sensible, usar navaja suave").
- **Portal del Empleado:** Solicitud automatizada de ausencias/faltas.
- **Rendimiento:** Visualización de ingresos generados y valoración media obtenida a través de las reseñas.

### 👤 Cliente
- **Reservas Inteligentes:** Sistema de *booking* que cruza disponibilidad de locales, horarios de barberos, días laborales y citas preexistentes para evitar solapamientos.
- **Catálogo de Sucursales:** Exploración de locales disponibles y puntuación media de sus barberos.
- **Fidelización:** Sistema de cupones automáticos basados en el historial de asistencia (ej. descuento cada 5 cortes).
- **Feedback:** Posibilidad de valorar y dejar reseñas en citas completadas.

## 🛠️ Arquitectura y Tecnologías Actuales

El prototipo se apoya en un stack ligero pero robusto para entorno de consola:
- **Python:** Lenguaje principal del proyecto.
- **Pydantic:** Utilizado exhaustivamente en el módulo `models/` para garantizar que los datos entrantes (fechas, UUIDs, correos, tipos de datos) sean estrictamente válidos antes de procesarlos.
- **Bcrypt (Passlib):** Hasheo de contraseñas para garantizar la seguridad de las credenciales desde la fase de prototipo.
- **Inquirer:** Librería para menús interactivos, limpios y amigables en la terminal.
- **JSON (BBDD Simulada):** Operaciones CRUD genéricas (`funciones/general/crud_generico.py`) que interactúan con archivos `.json` para simular tablas relacionales (Locales, Usuarios, Citas, Ausencias, Reseñas).

## 📂 Estructura del Proyecto

```text
Proyecto_administrador_Barberia_py/
├── main.py                  # Punto de entrada de la aplicación
├── requirements.txt         # Dependencias del proyecto
├── models/                  # Modelos de datos y validación (Pydantic)
│   ├── ausencia.py, cita.py, local.py, reseña.py, schemas.py
├── menu/                    # Lógica de interfaz de usuario CLI (Inquirer)
│   ├── menus_secundarios/   # Submenús modulares divididos por rol
│   └── m_principal.py       # Orquestador del menú principal
├── funciones/               # Lógica de negocio y utilidades
│   ├── general/             # CRUD JSON, arte ASCII, utilidades de consola
│   └── sesion/              # Manejo de estado de sesión y criptografía (hashes)
└── Data/                    # Almacenamiento persistente (Base de datos simulada)
    ├── ausencias.json, citas.json, locales.json, usuarios.json, etc.
```

## ⚙️ Instalación y Ejecución

1. **Clonar el repositorio** y navegar a la carpeta del proyecto.
2. **Crear y activar un entorno virtual** (Recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecutar el sistema:**
   ```bash
   python main.py
   ```

### 🔑 Usuarios de Prueba

Puedes probar los diferentes roles ingresando con las siguientes credenciales (extraídas de los datos por defecto):

* **Administrador General:** `fabianlv1920@gmail.com` | Pass: `admin123`
* **Administrador Local:** `isabel.castillo@example.com` | Pass: `Isabel2026!`
* **Barbero:** `roberto.g@example.com` | Pass: `RobertoBarber2`
* **Cliente:** `ana.gp@example.com` | Pass: `AnaCliente10`

---

## 🚀 Hacia un ERP Completo (Roadmap a Futuro)

Este proyecto está estructurado estratégicamente para que la transición de aplicación de consola a una plataforma backend escalable sea fluida. La evolución planificada contempla:

1. **Migración a Base de Datos Relacional:** Transición del sistema actual basado en archivos JSON hacia un motor **MySQL**. Las relaciones actuales (ID de locales, ID de empleados en las citas) se mapearán naturalmente a claves foráneas.
2. **Transición a Arquitectura API REST:** Integración del ecosistema actual con **FastAPI**. El enrutamiento modular (`routers`) reemplazará la carpeta `menu/`, separando los endpoints para usuarios, citas, ausencias y métricas. Los modelos actuales en `models/` ya están listos para FastAPI al estar basados en *Pydantic*.
3. **Autenticación y Seguridad:** Evolución del sistema de sesión en memoria actual hacia validación basada en tokens **JWT** usando librerías como `jose`, controlando la caducidad y el paso de tokens mediante redirecciones o *headers* HTTP.
4. **Desarrollo Frontend:** Una vez levantado el backend, la interfaz de CLI será sustituida por un cliente web (React/Vue) o aplicación móvil, consumiendo los datos estandarizados que el sistema ya es capaz de procesar.
```
