from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.route import Route
from app.schemas.route_schema import RouteCreate
from app.services.deps import get_admin_user

router = APIRouter(prefix="/api/routes", tags=["Routes"])

# 🔐 Admin - Create Route
@router.post("/")
def create_route(
    route: RouteCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    new_route = Route(
        name=route.name,
        source=route.source,
        destination=route.destination
    )

    db.add(new_route)
    db.commit()

    return {"message": "Route created successfully"}

# 👀 Public - View Routes
@router.get("/")
def get_routes(db: Session = Depends(get_db)):
    return db.query(Route).all()

from app.models.stop import Stop

@router.get("/{route_id}/stops")
def get_route_stops(route_id: int, db: Session = Depends(get_db)):
    route = db.query(Route).filter(Route.id == route_id).first()

    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    stops = db.query(Stop).filter(Stop.route_id == route_id).all()

    return {
        "route": route.name,
        "source": route.source,
        "destination": route.destination,
        "stops": stops
    }