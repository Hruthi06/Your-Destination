from pydantic import BaseModel
from typing import Optional

class BusCreate(BaseModel):
    bus_number: str
    driver_name: str
    capacity: int
    status: Optional[str] = "RUNNING"
    route_id: Optional[int] = None

class BusUpdate(BaseModel):
    bus_number: str
    driver_name: str
    capacity: int
    status: Optional[str] = "RUNNING"
    route_id: Optional[int] = None