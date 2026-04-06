from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, categories, transactions

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Expenses Manager",
    description="Backend for flutter App with ML predictions",
    version="1.0.0"
)

# Incluir todos los routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)

@app.get("/")
def read_root():
    return {
        "mensaje": "API funcionando",
        "documentacion": "/docs",
        "endpoints_disponibles": [
            "/usuarios",
            "/categories",
            "/transactions"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}