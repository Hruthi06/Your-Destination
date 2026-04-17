from sqlalchemy import Column, Integer, String
from app.database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String(50), unique=True)
    driver_name = Column(String(100))
    capacity = Column(Integer)