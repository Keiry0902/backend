#configuracion de la base de datp

#Se usa para conectarse a la base de datos (en este caso, PostgreSQL)
from sqlalchemy import create_engine
#se usa para definir clases como modelos de las tablas SQL.
from sqlalchemy.ext.declarative import declarative_base
#se usa para crear sesiones de base de datos (como conexiones temporales para leer/escribir datos).
from sqlalchemy.orm import sessionmaker
#permite cargar variables de entorno desde un archivo .env.
from dotenv import load_dotenv
import os

load_dotenv()

#Carga automáticamente las variables definidas en un archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")


#Crea el motor de conexión a la base de datos usando SQLAlchemy, para realizar todas las operaciones con SQL
engine = create_engine(DATABASE_URL)
#crea una clase sesión que puedes usar para conectarte a la base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Crea la base para todos los modelos de tablas.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()