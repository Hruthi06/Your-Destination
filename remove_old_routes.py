import sys, os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

def remove_routes():
    print("Removing old default routes...")
    
    # We'll search for routes starting with "Route "
    try:
        # Get route IDs first to clean up related data
        routes_to_delete = db.execute(text("SELECT id, name FROM routes WHERE name LIKE 'Route %'")).fetchall()
        
        if not routes_to_delete:
            print("No routes matching 'Route %' found.")
            return

        route_ids = [r[0] for r in routes_to_delete]
        print(f"Found {len(route_ids)} routes to delete.")

        # Disable checks to delete related data easily
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Delete related data for these routes
        for rid in route_ids:
            # Delete favorites
            db.execute(text("DELETE FROM favorites WHERE route_id = :rid"), {"rid": rid})
            # Delete stops
            db.execute(text("DELETE FROM stops WHERE route_id = :rid"), {"rid": rid})
            # Delete locations for buses on these routes
            db.execute(text("""
                DELETE FROM locations WHERE bus_id IN (SELECT id FROM buses WHERE route_id = :rid)
            """), {"rid": rid})
            # Delete buses
            db.execute(text("DELETE FROM buses WHERE route_id = :rid"), {"rid": rid})
            # Finally delete the route
            db.execute(text("DELETE FROM routes WHERE id = :rid"), {"rid": rid})
            
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        db.commit()
        print("Successfully removed old routes and their associated data.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during removal: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    remove_routes()
