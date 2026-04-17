from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserRegister, UserLogin
from app.services.auth_service import hash_password, verify_password
from app.config.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
    name=user.name,
    email=user.email,
    password=hash_password(user.password),
    role="USER"   
)
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/admin/login")
def admin_login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    # ❌ Wrong email or password
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ❌ Not an admin
    if db_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Access denied: Admins only")

    # ✅ Create token
    token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role
    }