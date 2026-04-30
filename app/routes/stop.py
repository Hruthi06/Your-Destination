from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stop import Stop
from app.schemas.stop_schema import StopCreate
from app.services.deps import get_admin_user

router = APIRouter(prefix="/api/stops", tags=["Stops"])

# 🔐 Admin - Create Stop
@router.post("/")
def create_stop(
    stop: StopCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    new_stop = Stop(
        name=stop.name,
        latitude=stop.latitude,
        longitude=stop.longitude,
        route_id=stop.route_id
    )

    db.add(new_stop)
    db.commit()

    return {"message": "Stop created successfully"}

# 👀 Public - Get Stops
@router.get("/")
def get_stops(db: Session = Depends(get_db)):
    return db.query(Stop).all()

@router.delete("/{stop_id}")
def delete_stop(
    stop_id: int, 
    db: Session = Depends(get_db), 
    admin=Depends(get_admin_user)
):
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    db.delete(stop)
    db.commit()
    return {"message": "Stop deleted successfully"}