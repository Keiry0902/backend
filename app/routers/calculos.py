from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.models import GestOdont, ApiOutput, Comparative
from app.database import SessionLocal

router = APIRouter()

# Conexion con la base de datos

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Todos los registros con diferencia calculada
@router.get("/registros-con-diferencia")
def registros_con_diferencia(encargado: str = None, year: int = None, month: int = None, day: int = None, db: Session = Depends(get_db)):
    query = (
        db.query(
            GestOdont.id_number,
            GestOdont.name,
            GestOdont.consult_date,
            GestOdont.assistant,
            GestOdont.register_value.label("pagado"),
            Comparative.expected_value.label("esperado"),
            (GestOdont.register_value - Comparative.expected_value).label("diferencia"),
            ApiOutput.status.label("estado")
        )
        .join(ApiOutput, GestOdont.id_number == ApiOutput.id_number)
        .join(Comparative, 
              (ApiOutput.regime == Comparative.regime) &
              (ApiOutput.affiliate_type == Comparative.affiliate_type) &
              (ApiOutput.category == Comparative.category))
    )

    if encargado:
        query = query.filter(GestOdont.assistant == encargado)
    if year:
        query = query.filter(extract("year", GestOdont.consult_date) == year)
    if month:
        query = query.filter(extract("month", GestOdont.consult_date) == month)
    if day:
        query = query.filter(extract("day", GestOdont.consult_date) == day)

    return query.all()

# 2. Total pagado
@router.get("/total-pagado")
def total_pagado(encargado: str = None, year: int = None, month: int = None, day: int = None, db: Session = Depends(get_db)):
    query = db.query(func.sum(GestOdont.register_value))
    if encargado:
        query = query.filter(GestOdont.assistant == encargado)
    if year:
        query = query.filter(extract("year", GestOdont.consult_date) == year)
    if month:
        query = query.filter(extract("month", GestOdont.consult_date) == month)
    if day:
        query = query.filter(extract("day", GestOdont.consult_date) == day)
    return {"total_pagado": query.scalar()}

# 3. Total esperado
@router.get("/total-esperado")
def total_esperado(encargado: str = None, year: int = None, month: int = None, day: int = None, db: Session = Depends(get_db)):
    query = (
        db.query(func.sum(Comparative.expected_value))
        .join(ApiOutput, (ApiOutput.regime == Comparative.regime) & (ApiOutput.affiliate_type == Comparative.affiliate_type) & (ApiOutput.category == Comparative.category))
        .join(GestOdont, GestOdont.id_number == ApiOutput.id_number)
    )

    if encargado:
        query = query.filter(GestOdont.assistant == encargado)
    if year:
        query = query.filter(extract("year", GestOdont.consult_date) == year)
    if month:
        query = query.filter(extract("month", GestOdont.consult_date) == month)
    if day:
        query = query.filter(extract("day", GestOdont.consult_date) == day)

    return {"total_esperado": query.scalar()}

# 4. Total diferencia
@router.get("/total-diferencia")
def total_diferencia(encargado: str = None, year: int = None, month: int = None, day: int = None, db: Session = Depends(get_db)):
    query = (
        db.query(func.sum(GestOdont.register_value - Comparative.expected_value))
        .join(ApiOutput, GestOdont.id_number == ApiOutput.id_number)
        .join(Comparative, 
              (ApiOutput.regime == Comparative.regime) &
              (ApiOutput.affiliate_type == Comparative.affiliate_type) &
              (ApiOutput.category == Comparative.category))
    )

    if encargado:
        query = query.filter(GestOdont.assistant == encargado)
    if year:
        query = query.filter(extract("year", GestOdont.consult_date) == year)
    if month:
        query = query.filter(extract("month", GestOdont.consult_date) == month)
    if day:
        query = query.filter(extract("day", GestOdont.consult_date) == day)

    return {"total_diferencia": query.scalar()}

