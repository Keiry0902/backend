from fastapi import FastAPI
from app.database import Base, engine
from app.routers import calculos 

# Crear tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(calculos.router)

# Agrega este bloque para que se pueda ejecutar con `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)