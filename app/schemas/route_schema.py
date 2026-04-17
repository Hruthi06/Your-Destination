from pydantic import BaseModel

class RouteCreate(BaseModel):
    name: str
    source: str
    destination: str