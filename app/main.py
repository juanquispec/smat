from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import api

# CREACIÓN DE LA BASE DE DATOS Y TABLAS
models.Base.metadata.create_all(bind=engine)

# Metadatos globales exactos solicitados por la rúbrica
app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="API robusta para la gestión y monitoreo de desastres naturales.\nPermite la telemetria de sensores en tiempo real y el cálculo de niveles de riesgo.\n\n**Entidades principales:**\n***Estaciones:** Puntos de monitoreo físico.\n***Lecturas:** Datos capturados por sensores.\n***Riesgos:** Análisis de criticidad basado en umbrales.",
    version="1.0.0",
    terms_of_service="http://unmsm.edu.pe/terms/",
    contact={
        "name": "Soporte Técnico SMAT - FISI",
        "url": "http://fisi.unmsm.edu.pe",
        "email": "desarrollo.smat@unmsm.edu.pe",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    }
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de submódulos
app.include_router(api.router)