from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.favorite import Favorite
from app.models.user import User
from app.models.route import Route
from app.schemas.favorite_schema import FavoriteCreate, FavoriteResponse
from app.services.deps import get_current_user
from typing import List

router = APIRouter(prefix="/api/user", tags=["User"])

@router.post("/favorites", response_model=FavoriteResponse)
def add_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_email = current_user.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    
    # Check if route exists
    route = db.query(Route).filter(Route.id == favorite.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Check if already exists
    existing = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.route_id == favorite.route_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")

    new_fav = Favorite(user_id=user.id, route_id=favorite.route_id)
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav

@router.get("/favorites", response_model=List[FavoriteResponse])
def get_favorites(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_email = current_user.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    return db.query(Favorite).filter(Favorite.user_id == user.id).all()

@router.delete("/favorites/{route_id}")
def remove_favorite(route_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_email = current_user.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    
    fav = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.route_id == route_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(fav)
    db.commit()
    return {"message": "Removed from favorites"}
