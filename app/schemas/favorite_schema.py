from pydantic import BaseModel

class FavoriteBase(BaseModel):
    route_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
