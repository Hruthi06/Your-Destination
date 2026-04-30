import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import math
import random
from app.database import SessionLocal
from app.models import bus as bus_model
from app.models.stop import Stop as StopModel
from app.models.location import Location as LocationModel

bus_directions = {} # bus_id -> 1 (forward), -1 (backward)

def simulate():
    print("🚀 Standalone Continuous Simulation started...")
    while True:
        db = SessionLocal()
        try:
            buses = db.query(bus_model.Bus).filter(bus_model.Bus.status == "RUNNING").all()
            for bus in buses:
                if not bus.route_id: continue
                
                if bus.id not in bus_directions:
                    bus_directions[bus.id] = 1

                stops = db.query(StopModel).filter(StopModel.route_id == bus.route_id).order_by(StopModel.id).all()
                if not stops: continue
                num_stops = len(stops)

                loc = db.query(LocationModel).filter(LocationModel.bus_id == bus.id).order_by(LocationModel.timestamp.desc()).first()
                if not loc:
                    db.add(LocationModel(bus_id=bus.id, latitude=stops[0].latitude, longitude=stops[0].longitude))
                    db.commit()
                    continue

                # Find closest stop
                dists = [math.sqrt((loc.latitude - s.latitude)**2 + (loc.longitude - s.longitude)**2) for s in stops]
                closest_idx = dists.index(min(dists))
                
                # Check if at stop
                if dists[closest_idx] < 0.0003:
                    loc.latitude = stops[closest_idx].latitude
                    loc.longitude = stops[closest_idx].longitude
                    db.commit()
                    
                    if closest_idx == num_stops - 1:
                        bus_directions[bus.id] = -1
                    elif closest_idx == 0:
                        bus_directions[bus.id] = 1
                    continue

                # Move toward target
                direction = bus_directions[bus.id]
                target_idx = closest_idx + direction
                if target_idx >= num_stops: target_idx = num_stops - 1
                if target_idx < 0: target_idx = 0
                
                target_stop = stops[target_idx]
                prev_stop = stops[closest_idx]
                
                total_leg_dist = math.sqrt((target_stop.latitude - prev_stop.latitude)**2 + (target_stop.longitude - prev_stop.longitude)**2)
                speed_factor = random.uniform(0.8, 1.2)
                step = (total_leg_dist / 10.0) * speed_factor
                if step == 0: step = 0.0005 

                angle = math.atan2(target_stop.latitude - loc.latitude, target_stop.longitude - loc.longitude)
                new_lat = loc.latitude + math.sin(angle) * step
                new_lng = loc.longitude + math.cos(angle) * step
                
                db.add(LocationModel(bus_id=bus.id, latitude=new_lat, longitude=new_lng))
                db.commit()
                print(f"Bus {bus.bus_number} moving {'Forward' if direction==1 else 'Backward'}")

        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            db.close()
        time.sleep(3)

if __name__ == "__main__":
    simulate()
