from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.location import Location
from app.models.bus import Bus
from app.schemas.location_schema import LocationUpdate
from app.services.deps import get_admin_user

router = APIRouter(prefix="/api/location", tags=["Tracking"])

# 🔐 Admin - Update Location
@router.post("/update")
def update_location(
    data: LocationUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    bus = db.query(Bus).filter(Bus.id == data.bus_id).first()

    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    new_location = Location(
        bus_id=data.bus_id,
        latitude=data.latitude,
        longitude=data.longitude
    )

    db.add(new_location)
    db.commit()

    return {"message": "Location updated"}


# 👀 Public - Get Latest Location
@router.get("/{bus_id}")
def get_location(bus_id: int, db: Session = Depends(get_db)):
    location = db.query(Location)\
        .filter(Location.bus_id == bus_id)\
        .order_by(Location.timestamp.desc())\
        .first()

    if not location:
        raise HTTPException(status_code=404, detail="No location found")

    return {
        "bus_id": bus_id,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "timestamp": location.timestamp
    }