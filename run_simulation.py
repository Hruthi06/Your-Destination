import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import math
import random
from app.database import SessionLocal
from app.models import bus as bus_model
from app.models.stop import Stop as StopModel
from app.models.location import Location as LocationModel

waiting_buses = {} # bus_id -> wait_until_timestamp
bus_directions = {} # bus_id -> 1 (forward), -1 (backward)
bus_targets = {} # bus_id -> target_stop_index

def simulate():
    print("Standalone Continuous Simulation started...")
    while True:
        db = SessionLocal()
        try:
            now = time.time()
            buses = db.query(bus_model.Bus).filter(bus_model.Bus.status == "RUNNING").all()
            for bus in buses:
                if not bus.route_id: continue
                
                # Default direction: Forward
                if bus.id not in bus_directions:
                    bus_directions[bus.id] = 1

                # Check if waiting at a station
                if bus.id in waiting_buses:
                    if now < waiting_buses[bus.id]: continue
                    else: del waiting_buses[bus.id]

                stops = db.query(StopModel).filter(StopModel.route_id == bus.route_id).order_by(StopModel.id).all()
                if not stops: continue
                num_stops = len(stops)

                loc = db.query(LocationModel).filter(LocationModel.bus_id == bus.id).order_by(LocationModel.id.desc()).first()
                if not loc:
                    db.add(LocationModel(bus_id=bus.id, latitude=stops[0].latitude, longitude=stops[0].longitude))
                    db.commit()
                    continue

                # Initialize target if not set
                if bus.id not in bus_targets or bus_targets[bus.id] >= num_stops:
                    dists = [math.sqrt((loc.latitude - s.latitude)**2 + (loc.longitude - s.longitude)**2) for s in stops]
                    closest_idx = dists.index(min(dists))
                    direction = bus_directions[bus.id]
                    target_idx = closest_idx + direction
                    if target_idx >= num_stops:
                        target_idx = num_stops - 1
                        bus_directions[bus.id] = -1
                    elif target_idx < 0:
                        target_idx = 0
                        bus_directions[bus.id] = 1
                    bus_targets[bus.id] = target_idx

                target_idx = bus_targets[bus.id]
                target_stop = stops[target_idx]

                # Distance to target stop
                dist_to_target = math.sqrt((loc.latitude - target_stop.latitude)**2 + (loc.longitude - target_stop.longitude)**2)
                
                # Check if we have REACHED the current target stop
                if dist_to_target < 0.0003:
                    # We are at the stop! snap to it
                    loc.latitude = target_stop.latitude
                    loc.longitude = target_stop.longitude
                    db.commit()
                    
                    # Determine next direction
                    if target_idx == num_stops - 1:
                        bus_directions[bus.id] = -1
                    elif target_idx == 0:
                        bus_directions[bus.id] = 1
                    
                    # Set next target stop index
                    direction = bus_directions[bus.id]
                    next_target_idx = target_idx + direction
                    if next_target_idx >= num_stops: next_target_idx = num_stops - 1
                    if next_target_idx < 0: next_target_idx = 0
                    bus_targets[bus.id] = next_target_idx
                    
                    # Wait 6 seconds (2 ticks) at the stop
                    waiting_buses[bus.id] = now + 6
                    print(f"Bus {bus.bus_number} reached stop {target_stop.name}, waiting...")
                    continue

                # Movement Logic: step towards target stop
                prev_stop_idx = target_idx - bus_directions[bus.id]
                if prev_stop_idx < 0: prev_stop_idx = 0
                if prev_stop_idx >= num_stops: prev_stop_idx = num_stops - 1
                prev_stop = stops[prev_stop_idx]

                total_leg_dist = math.sqrt((target_stop.latitude - prev_stop.latitude)**2 + (target_stop.longitude - prev_stop.longitude)**2)
                speed_factor = random.uniform(0.8, 1.2)
                step = (total_leg_dist / 10.0) * speed_factor
                if step == 0: step = 0.0005 

                angle = math.atan2(target_stop.latitude - loc.latitude, target_stop.longitude - loc.longitude)
                new_lat = loc.latitude + math.sin(angle) * step
                new_lng = loc.longitude + math.cos(angle) * step
                
                # Prevent overshooting target
                dist_to_target_after_step = math.sqrt((target_stop.latitude - new_lat)**2 + (target_stop.longitude - new_lng)**2)
                if dist_to_target_after_step < step:
                    new_lat = target_stop.latitude
                    new_lng = target_stop.longitude
                
                db.add(LocationModel(bus_id=bus.id, latitude=new_lat, longitude=new_lng))
                db.commit()
                print(f"Bus {bus.bus_number} moving towards {target_stop.name}")

        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            db.close()
        time.sleep(3)

if __name__ == "__main__":
    simulate()
