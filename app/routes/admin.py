from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.bus import Bus
from app.models.route import Route
from app.models.stop import Stop
from app.services.deps import get_admin_user
from app.schemas.user_schema import UserResponse
from typing import List

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    total_users = db.query(User).count()
    total_buses = db.query(Bus).count()
    active_buses = db.query(Bus).filter(Bus.status == "RUNNING").count()
    total_routes = db.query(Route).count()
    total_stops = db.query(Stop).count()

    return {
        "total_users": total_users,
        "total_buses": total_buses,
        "active_buses": active_buses,
        "total_routes": total_routes,
        "total_stops": total_stops
    }

@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    return db.query(User).all()

@router.put("/users/{user_id}/toggle-block")
def toggle_block_user(user_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email == admin.get("sub"):
         raise HTTPException(status_code=400, detail="You cannot block yourself")

    user.is_blocked = not user.is_blocked
    db.commit()
    return {"message": f"User {'blocked' if user.is_blocked else 'unblocked'} successfully", "is_blocked": user.is_blocked}
