from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db
models.Base.metadata.create_all(bind=engine)

# 1
app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="""
    API para la gestión de desastres naturales y telemetría de sensores en tiempo real.
    **Entidades:** Estaciones, Lecturas y Análisis de Riesgos.
    """,
    version="1.0.0",
    contact={
        "name": "Soporte Técnico SMAT - FISI",
        "url": "http://fisi.unmsm.edu.pe",
        "email": "desarrollo.smat@unmsm.edu.pe",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float

# 2
@app.post(
    "/estaciones/", 
    status_code=201, 
    tags=["Gestión de Infraestructura"],
    summary="Registrar una nueva estación",
    description="Inserta una estación física en la base de datos relacional."
)
def crear_estacion(estacion: EstacionCreate, db: Session = Depends(get_db)):
    nueva_estacion = models.EstacionDB(id=estacion.id, nombre=estacion.nombre, ubicacion=estacion.ubicacion)
    db.add(nueva_estacion)
    db.commit()
    db.refresh(nueva_estacion)
    return {"msj": "Estación guardada", "data": nueva_estacion}

@app.post(
    "/lecturas/", 
    status_code=201, 
    tags=["Telemetría de Sensores"],
    summary="Recibir datos de telemetría",
    description="Recibe el valor de un sensor y lo vincula a una estación mediante su ID."
)
def registrar_lectura(lectura: LecturaCreate, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == lectura.estacion_id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    nueva_lectura = models.LecturaDB(valor=lectura.valor, estacion_id=lectura.estacion_id)
    db.add(nueva_lectura)
    db.commit()
    return {"status": "Lectura guardada"}

# 3
@app.get(
    "/estaciones/{id}/historial",
    tags=["Reportes Históricos"],
    summary="Consultar historial de lecturas",
    description="Obtiene todas las mediciones de una estación. Realiza cálculos estadísticos de conteo y promedio.",
    responses={404: {"description": "Estación no encontrada"}}
)
def obtener_historial(id: int, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(models.EstacionDB.id == id).first()
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    historial = db.query(models.LecturaDB).filter(models.LecturaDB.estacion_id == id).all()
    return {"estacion_id": id, "total": len(historial), "historial": historial}