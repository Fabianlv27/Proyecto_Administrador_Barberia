from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union
from datetime import date

# --- Clase Base ---
class Persona(BaseModel):
    id: str  # El UUID
    nombre: str
    apellido: str
    numero: str
    correo: EmailStr
    contraseña: str  # Hash SHA-256
    rol: List[str]
    DNI: Optional[str] = None
    Ciudad: Optional[str] = None
    Provincia: Optional[str] = None
    codigo_postal: Optional[int] = None
    direccion: Optional[str] = None
    informacion_adicional: Optional[str] = None

# --- Mixin para Roles de Trabajo (Admin, Empleado, Barbero) ---
class DatosLaborales(BaseModel):
    estado: Optional[str] = "Trabajando"
    sueldo: Optional[float] = 0.0
    local: Optional[str] = None
    dia_inicio: Optional[Union[date, str]] = None
    dia_fin: Optional[str] = "indefinido"
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    dias_semanas: Optional[str] = None # Ejemplo: "LMXJV"

# --- Mixin para Roles de Cliente ---
class DatosConsumo(BaseModel):
    n_citas: int = 0
    total_gasto: float = 0.0
    citas: List[str] = []
    local_favorito: Optional[str] = None
    barberos_favorito: List[str] = []

# --- Clases Finales (Modelos de Dominio) ---

class Empleado(Persona, DatosLaborales):
    """Aplica para empleados, barberos y administradores locales"""
    cargos: List[str] = []
    experiecia: Optional[str] = None
    total_generado: Optional[float] = 0.0
    reseñas: List[str] = []

class Cliente(Persona, DatosConsumo):
    """Aplica para usuarios con rol único de cliente"""
    pass

class AdminGeneral(Persona, DatosLaborales):
    """Aplica para el dueño o administradores globales"""
    pass