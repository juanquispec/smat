from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter()

@router.post("/token", tags=["Seguridad"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "secret":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.crear_token_acceso(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/estaciones/", status_code=201, tags=["Estaciones"])
def crear_estacion(
    estacion: schemas.EstacionCreate, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(auth.obtener_identidad_actual)
):
    db_estacion = crud.obtener_estacion(db, estacion_id=estacion.id)
    if db_estacion:
        raise HTTPException(status_code=400, detail="La estación ya existe")
    nueva_estacion = crud.crear_estacion(db=db, estacion=estacion)
    return {"msj": "Estación guardada en DB", "data": nueva_estacion}

@router.get("/estaciones/", response_model=List[schemas.Estacion], tags=["Estaciones"])
def listar_estaciones(db: Session = Depends(get_db)):
    return crud.obtener_estaciones(db)

@router.post("/lecturas/", status_code=201, tags=["Lecturas"])
def registrar_lectura(
    lectura: schemas.LecturaCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.obtener_identidad_actual)
):
    estacion = crud.obtener_estacion(db, estacion_id=lectura.estacion_id)
    if not estacion:
        raise HTTPException(status_code=404, detail="Error de Integridad: La estación no existe en la base de datos.")
    crud.crear_lectura(db=db, lectura=lectura)
    return {"status": "Lectura guardada en DB"}

@router.get("/estaciones/{id}/historial", tags=["Reportes Históricos"], summary="Obtener historial de lecturas", description="Devuelve el historial completo de lecturas de una estación. Calcula estadísticamente el conteo total de datos y el promedio aritmético de los valores.", responses={404: {"description": "Estación no encontrada"}})
def obtener_historial(id: int, db: Session = Depends(get_db)):
    estacion = crud.obtener_estacion(db, estacion_id=id)
    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    lecturas_filtradas = crud.obtener_lecturas_por_estacion(db, estacion_id=id)
    valores = [l.valor for l in lecturas_filtradas]
    conteo = len(valores)
    
    if conteo > 0:
        promedio = sum(valores) / conteo
    else:
        promedio = 0.0
        
    return {
        "estacion_id": id,
        "lecturas": valores,
        "conteo": conteo,
        "promedio": round(promedio, 2)
    }

@router.get("/reportes/criticos", tags=["Auditoria"], summary="Reportes Críticos", description="Analiza las lecturas y evalúa la severidad filtrando a través del parámetro opcional 'umbral', permitiendo ignorar valores bajos.")
def reportes_criticos(umbral: float = 10.0, db: Session = Depends(get_db)):
    return {"mensaje": f"Reporte de lecturas superiores al umbral de {umbral}"}

@router.get("/estaciones/stats", tags=["Estaciones"], summary="Estadísticas de Sistema", description="Resumen ejecutivo del sistema que expone de forma global el estado general de la infraestructura y el conteo.")
def estaciones_stats(db: Session = Depends(get_db)):
    estaciones = crud.obtener_estaciones(db)
    return {"total_estaciones_registradas": len(estaciones)}