from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class Reseña(BaseModel):
    id_reseña: str
    id_cita: str      # Cada reseña debe estar vinculada a una cita real
    id_cliente: str
    id_barbero: str
    puntuacion: int = Field(ge=1, le=5) # Escala del 1 al 5
    comentario: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.now)
    visible: bool = True