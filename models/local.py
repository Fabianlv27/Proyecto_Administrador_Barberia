from pydantic import BaseModel, Field
from typing import List, Optional

class Local(BaseModel):
    id_local: str = Field(description="ID único del local, ej: AAA88")
    nombre: str
    direccion: str
    ciudad: str
    provincia: str
    codigo_postal: int
    telefono: str
    capacidad_barberos: int
    servicios_disponibles: List[str]  # ["Corte", "Barba", "Tinte"]
    horario_apertura: str  # "09:00"
    horario_cierre: str    # "20:00"
    activo: bool = True