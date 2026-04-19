from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    route_id = Column(Integer, ForeignKey("routes.id"))
    