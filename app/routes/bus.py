from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.bus import Bus
from app.schemas.bus_schema import BusCreate
from app.services.deps import get_admin_user

# ✅ ADD THIS (you missed this)
router = APIRouter(prefix="/api/buses", tags=["Bus"])


# 🔐 Admin Only - Create Bus
@router.post("/")
def create_bus(
    bus: BusCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    existing = db.query(Bus).filter(Bus.bus_number == bus.bus_number).first()

    if existing:
        raise HTTPException(status_code=400, detail="Bus already exists")

    new_bus = Bus(
        bus_number=bus.bus_number,
        driver_name=bus.driver_name,
        capacity=bus.capacity
    )

    db.add(new_bus)
    db.commit()

    return {"message": "Bus created successfully"}


# 👀 Public - Get Buses
@router.get("/")
def get_buses(db: Session = Depends(get_db)):
    buses = db.query(Bus).all()
    return buses

from app.schemas.bus_schema import BusUpdate

@router.put("/{bus_id}")
def update_bus(
    bus_id: int,
    bus: BusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()

    if not db_bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    db_bus.bus_number = bus.bus_number
    db_bus.driver_name = bus.driver_name
    db_bus.capacity = bus.capacity

    db.commit()

    return {"message": "Bus updated successfully"}

@router.delete("/{bus_id}")
def delete_bus(
    bus_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    db_bus = db.query(Bus).filter(Bus.id == bus_id).first()

    if not db_bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    db.delete(db_bus)
    db.commit()

    return {"message": "Bus deleted successfully"}