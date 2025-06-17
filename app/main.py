from fastapi import FastAPI
from app.database import Base, engine
from app.routers import calculos 

# Crear tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(calculos.router)