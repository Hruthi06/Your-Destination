from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String(50), unique=True)
    driver_name = Column(String(100))
    capacity = Column(Integer)
    status = Column(String(20), default="RUNNING") # RUNNING, NOT_RUNNING, MAINTENANCE
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)