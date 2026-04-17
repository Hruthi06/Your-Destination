from pydantic import BaseModel

class BusCreate(BaseModel):
    bus_number: str
    driver_name: str
    capacity: int

class BusUpdate(BaseModel):
    bus_number: str
    driver_name: str
    capacity: int