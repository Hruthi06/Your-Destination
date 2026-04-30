from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_blocked: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str