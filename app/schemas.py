from pydantic import BaseModel
from typing import List

class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class Estacion(EstacionCreate):
    class Config:
        orm_mode = True

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float

class Lectura(LecturaCreate):
    id: int
    class Config:
        orm_mode = True