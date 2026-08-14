"""
Tumkur City Bus Routes Seeder
Seeds the database with real Tumkur KSRTC city bus routes,
stops with GPS coordinates, and 10 buses per route staggered 10 min apart.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

# ─────────────────────────────────────────────
# TUMKUR CITY BUS ROUTES with real GPS stops
# ─────────────────────────────────────────────
ROUTES = [
    {
        "name": "Route 1 – Kyathsandra to Heggere",
        "source": "Kyathsandra",
        "destination": "Heggere",
        "stops": [
            ("Kyathsandra Bus Stop",         13.3725, 77.1050),
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Townhall Circle",               13.3420, 77.1020),
            ("Siddaganga Mutt Gate",          13.3560, 77.0910),
            ("Upparahalli Circle",            13.3310, 77.0980),
            ("Heggere Village",              13.3210, 77.0900),
        ]
    },
    {
        "name": "Route 2 – Shettihalli to Yellapura",
        "source": "Shettihalli",
        "destination": "Yellapura",
        "stops": [
            ("Shettihalli Cross",             13.3640, 77.0780),
            ("B.G. Palya Circle",             13.3500, 77.0970),
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Old Bus Stand",                 13.3430, 77.1025),
            ("Navagraha Temple Stop",         13.3300, 77.1100),
            ("Yellapura Road End",            13.3200, 77.1200),
        ]
    },
    {
        "name": "Route 3 – Oorukere to Maralur Dinne",
        "source": "Oorukere",
        "destination": "Maralur Dinne",
        "stops": [
            ("Oorukere Lake Bus Stop",        13.3580, 77.1280),
            ("Kaveri School Stop",            13.3490, 77.1190),
            ("DC Office Circle",             13.3447, 77.1072),
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Gangasandra Road",              13.3350, 77.0900),
            ("Maralur Dinne",                13.3150, 77.0750),
        ]
    },
    {
        "name": "Route 4 – Tumkur to Siddaganga Mutt",
        "source": "KSRTC Bus Stand",
        "destination": "Siddaganga Mutt",
        "stops": [
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Townhall Bus Stop",             13.3420, 77.1050),
            ("Shankara Mutt Stop",           13.3480, 77.0960),
            ("SIT College Back Gate",         13.3520, 77.0930),
            ("Siddaganga Mutt Gate",          13.3560, 77.0910),
        ]
    },
    {
        "name": "Route 5 – Gangasandra to Belagumba",
        "source": "Gangasandra",
        "destination": "Belagumba",
        "stops": [
            ("Gangasandra Circle",            13.3650, 77.0830),
            ("RK Vivekananda Ashrama",        13.3560, 77.0960),
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Andrahalli Gate",               13.3300, 77.1050),
            ("Belagumba Village",             13.3100, 77.1150),
        ]
    },
    {
        "name": "Route 6 – Tumkur to Devarayapatna",
        "source": "KSRTC Bus Stand",
        "destination": "Devarayapatna",
        "stops": [
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("SIT Back Gate Stop",            13.3520, 77.0930),
            ("Upparahalli Gate",              13.3330, 77.0995),
            ("Goolarive Cross",               13.3250, 77.0920),
            ("Devarayapatna Village",         13.3050, 77.0840),
        ]
    },
    {
        "name": "Route 7 – Tumkur to Bellavi",
        "source": "KSRTC Bus Stand",
        "destination": "Bellavi",
        "stops": [
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Old Bus Stand",                 13.3430, 77.1025),
            ("Tumkur University Gate",        13.3460, 77.1280),
            ("Hirehalli Industrial Area",     13.3380, 77.1420),
            ("Bellavi Cross",                 13.3250, 77.1600),
        ]
    },
    {
        "name": "Route 8 – Tumkur to Kesaramadu",
        "source": "KSRTC Bus Stand",
        "destination": "Kesaramadu",
        "stops": [
            ("KSRTC Main Bus Stand",          13.3424, 77.1016),
            ("Townhall Circle",               13.3420, 77.1050),
            ("Kunigal Road Junction",         13.3480, 77.1200),
            ("Hebbur Cross",                  13.3550, 77.1350),
            ("Kesaramadu Village",            13.3670, 77.1500),
        ]
    },
]

# Driver names pool
DRIVERS = [
    "Raju Kumar", "Mohan Gowda", "Suresh Naik", "Ramesh BR", "Anil Kumar",
    "Prasad MK", "Venkatesh R", "Krishnamurthy", "Sunil Patil", "Deepak Rao",
    "Manjunath", "Sathish Kumar", "Nagaraj", "Basavaraju", "Chandrashekar",
    "Vijay Kumar", "Mahesh N", "Girish BM", "Harish PK", "Lokesh T",
    "Nagesh R", "Kiran Kumar", "Umesh S", "Dileep MV", "Santosh K",
]

driver_idx = 0
bus_num_prefix = 1000

def seed():
    global driver_idx, bus_num_prefix

    # Clear existing data in proper FK order
    print("Clearing existing data...")
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("DELETE FROM favorites"))
    db.execute(text("DELETE FROM locations"))
    db.execute(text("DELETE FROM stops"))
    db.execute(text("DELETE FROM buses"))
    db.execute(text("DELETE FROM routes"))
    
    # Reset auto_increment counters
    db.execute(text("ALTER TABLE favorites AUTO_INCREMENT = 1"))
    db.execute(text("ALTER TABLE locations AUTO_INCREMENT = 1"))
    db.execute(text("ALTER TABLE stops AUTO_INCREMENT = 1"))
    db.execute(text("ALTER TABLE buses AUTO_INCREMENT = 1"))
    db.execute(text("ALTER TABLE routes AUTO_INCREMENT = 1"))
    
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    db.commit()
    print("Cleared and auto-increment counters reset to 1.")

    for route_data in ROUTES:
        print(f"\nSeeding: {route_data['name']}")

        # 1. Create Route
        db.execute(text("""
            INSERT INTO routes (name, source, destination)
            VALUES (:name, :source, :destination)
        """), {
            "name": route_data["name"],
            "source": route_data["source"],
            "destination": route_data["destination"]
        })
        db.commit()
        route_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        print(f"  Route ID: {route_id}")

        # 2. Create Stops
        for stop_name, lat, lng in route_data["stops"]:
            db.execute(text("""
                INSERT INTO stops (name, latitude, longitude, route_id)
                VALUES (:name, :lat, :lng, :route_id)
            """), {"name": stop_name, "lat": lat, "lng": lng, "route_id": route_id})
        db.commit()
        print(f"  Added {len(route_data['stops'])} stops")

        # 3. Create 10 Buses per route
        for i in range(10):
            bus_number = f"KA-06-{bus_num_prefix + i}"
            driver = DRIVERS[driver_idx % len(DRIVERS)]
            driver_idx += 1

            db.execute(text("""
                INSERT INTO buses (bus_number, driver_name, capacity, status, route_id)
                VALUES (:bus_number, :driver_name, :capacity, :status, :route_id)
            """), {
                "bus_number": bus_number,
                "driver_name": driver,
                "capacity": 50,
                "status": "RUNNING",
                "route_id": route_id
            })
        db.commit()

        # Set bus_num_prefix for next route
        bus_num_prefix += 10

        # 4. Seed initial location for each bus at stop positions (staggered)
        buses = db.execute(text(
            "SELECT id FROM buses WHERE route_id = :rid ORDER BY id"
        ), {"rid": route_id}).fetchall()

        stops = route_data["stops"]
        total_stops = len(stops)

        for i, (bus_row,) in enumerate(buses):
            # Each bus is 1 stop apart on the route, cycling
            stop_idx = i % total_stops
            stop_name, lat, lng = stops[stop_idx]

            # Check if location entry exists
            existing = db.execute(text(
                "SELECT id FROM locations WHERE bus_id = :bid"
            ), {"bid": bus_row}).fetchone()

            if existing:
                db.execute(text("""
                    UPDATE locations SET latitude=:lat, longitude=:lng
                    WHERE bus_id=:bid
                """), {"lat": lat, "lng": lng, "bid": bus_row})
            else:
                db.execute(text("""
                    INSERT INTO locations (bus_id, latitude, longitude)
                    VALUES (:bid, :lat, :lng)
                """), {"bid": bus_row, "lat": lat, "lng": lng})
        db.commit()
        print(f"  Added 10 buses with initial locations (staggered across {total_stops} stops)")

    print("\n[SUCCESS] All Tumkur city bus routes seeded successfully!")
    total_routes = db.execute(text("SELECT COUNT(*) FROM routes")).scalar()
    total_buses  = db.execute(text("SELECT COUNT(*) FROM buses")).scalar()
    total_stops  = db.execute(text("SELECT COUNT(*) FROM stops")).scalar()
    print(f"  Routes: {total_routes}")
    print(f"  Buses:  {total_buses} ({total_buses // total_routes} per route)")
    print(f"  Stops:  {total_stops}")
    db.close()

if __name__ == "__main__":
    seed()
