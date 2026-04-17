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