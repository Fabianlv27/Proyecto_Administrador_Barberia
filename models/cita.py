from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Cita(BaseModel):
    id_cita: str = Field(description="ID único de la cita, ej: QWE73")
    id_cliente: str  # Referencia al UUID del usuario
    id_barbero: str  # Referencia al UUID del empleado
    id_local: str    # Referencia al ID del local
    fecha_hora: datetime
    servicio: str    # Ej: "Corte de pelo Degradado"
    duracion_minutos: int = 30
    precio: float
    estado: str = "Pendiente"  # "Pendiente", "Completada", "Cancelada", "No asistió"
    notas_barbero: Optional[str] = None