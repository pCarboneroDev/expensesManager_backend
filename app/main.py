from fastapi import FastAPI
from . import models
from .database import engine
from .routers import usuarios

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API para App Flutter",
    description="Backend con soporte para ML",
    version="1.0.0"
)

# Incluir todos los routers
app.include_router(usuarios.router)

@app.get("/")
def read_root():
    return {
        "mensaje": "API funcionando",
        "documentacion": "/docs",
        "endpoints_disponibles": [
            "/usuarios",
        ]
    }

@app.get("/health")
def health_check():
    """Endpoint para verificar que la API está viva"""
    return {"status": "healthy"}