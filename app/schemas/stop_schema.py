from pydantic import BaseModel

class StopCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    route_id: int