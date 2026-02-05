from datetime import date
from typing import Optional

from pydantic import BaseModel

class Ausencia(BaseModel):
    id_ausencia: str
    id_empleado: str
    tipo: str  # "Vacaciones", "Enfermedad", "Asuntos Propios"
    fecha_inicio: date
    fecha_fin: date
    aprobada: bool = False
    comentario: Optional[str] = None    