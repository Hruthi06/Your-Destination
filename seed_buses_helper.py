from app.database import SessionLocal
from app.models.route import Route
from app.models.bus import Bus
from app.models.location import Location
from app.models.stop import Stop

def seed_buses():
    db = SessionLocal()
    routes = db.query(Route).all()
    if not routes:
        print("No routes found to seed buses.")
        return

    for r in routes:
        # Check if bus already exists
        existing = db.query(Bus).filter(Bus.route_id == r.id).first()
        if not existing:
            bus = Bus(
                bus_number=f"KA-06-B-{1000 + r.id}",
                driver_name="Simulated Driver",
                capacity=50,
                status="RUNNING",
                route_id=r.id
            )
            db.add(bus)
            db.flush()
            
            # Also add an initial location at the first stop
            first_stop = db.query(Stop).filter(Stop.route_id == r.id).order_by(Stop.id).first()
            if first_stop:
                loc = Location(
                    bus_id=bus.id,
                    latitude=first_stop.latitude,
                    longitude=first_stop.longitude
                )
                db.add(loc)
            
            print(f"Added bus and initial location for route: {r.name}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_buses()
