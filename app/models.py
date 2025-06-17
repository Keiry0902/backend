from sqlalchemy import Column, Integer, String, Date, Time, Numeric, ForeignKey, PrimaryKeyConstraint
from app.database import Base

class GestOdont(Base):
    __tablename__ = "gest_odont"

    id_number = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    consult_date = Column(Date, nullable=False)
    consult_time = Column(Time, nullable=False)
    assistant = Column(String(80), nullable=False)
    consult_type = Column(String(50), nullable=False)
    register_value = Column(Numeric(10,2), nullable=False)

class ApiOutput(Base):
    __tablename__ = "api_output"

    id_number = Column(Integer, primary_key=True)
    status = Column(String(20), nullable=False)
    entity = Column(String(50), nullable=False)
    regime = Column(String(20), nullable=False)
    affiliate_type = Column(String(20), nullable=False)
    category = Column(String(1), nullable=False)

class Comparative(Base):
    __tablename__ = "comparative"

    regime = Column(String(20), nullable=False)
    affiliate_type = Column(String(20), nullable=False)
    category = Column(String(1), nullable=False)
    expected_value = Column(Numeric(10,2), nullable=False)

    __table_args__ = (PrimaryKeyConstraint('regime', 'affiliate_type', 'category'),)