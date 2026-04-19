from pydantic import BaseModel

class LocationUpdate(BaseModel):
    bus_id: int
    latitude: float
    longitude: float