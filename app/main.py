from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models import bus as bus_model
from app.models import route as route_model
from app.models.stop import Stop as StopModel
from app.models.location import Location as LocationModel
from app.services.auth_service import hash_password
from app.routes import auth, bus, route, stop, location, admin, user_api

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import threading
import time
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("assets"):
    os.makedirs("assets")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

Base.metadata.create_all(bind=engine)

app.include_router(stop.router)
app.include_router(auth.router)
app.include_router(bus.router)
app.include_router(route.router)
app.include_router(location.router)
app.include_router(admin.router)
app.include_router(user_api.router)

@app.get("/")
@app.get("/login")
def login_page():
    return FileResponse("login.html")

@app.get("/user")
@app.get("/user.html")
@app.get("/index.html")
@app.get("/tracking")
def user_dashboard():
    return FileResponse("user.html")

@app.get("/map")
@app.get("/map.html")
def view_map():
    return FileResponse("map.html")

@app.get("/admin")
@app.get("/admin.html")
def view_admin():
    return FileResponse("admin.html")

@app.get("/bus_selection")
@app.get("/bus_selection.html")
def bus_selection_page():
    return FileResponse("bus_selection.html")

@app.get("/admin/login")
def admin_login_page():
    return FileResponse("admin_login.html")

def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin@admin.com").first()
    if not admin:
        new_admin = User(
            name="Admin", email="admin@admin.com",
            password=hash_password("admin123"), role="ADMIN"
        )
        db.add(new_admin)
        db.commit()
    db.close()

# ✅ Simulation Logic
waiting_buses = {} # bus_id -> wait_until_timestamp
bus_directions = {} # bus_id -> 1 (forward), -1 (backward)

def simulate_buses():
    print("🚀 Bus simulation engine starting...")
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
                loc = db.query(LocationModel).filter(LocationModel.bus_id == bus.id).order_by(LocationModel.timestamp.desc()).first()
                if not loc:
                    db.add(LocationModel(bus_id=bus.id, latitude=stops[0].latitude, longitude=stops[0].longitude))
                    db.commit()
                    continue

                # Find which stop we are currently at or closest to
                dists = [math.sqrt((loc.latitude - s.latitude)**2 + (loc.longitude - s.longitude)**2) for s in stops]
                closest_idx = dists.index(min(dists))
                
                # Check if we have REACHED the current target stop
                if dists[closest_idx] < 0.0003:
                    # We are at a stop! 
                    # 1. Snap to it
                    loc.latitude = stops[closest_idx].latitude
                    loc.longitude = stops[closest_idx].longitude
                    db.commit()
                    
                    # 2. Check if we need to reverse direction (Continuous movement, no waiting)
                    if closest_idx == num_stops - 1:
                        bus_directions[bus.id] = -1 # Reverse to backward
                    elif closest_idx == 0:
                        bus_directions[bus.id] = 1 # Reverse to forward
                    
                    # NO WAIT TIME - Continue moving instantly
                    # waiting_buses[bus.id] = now + 30 
                    
                    continue

                # Movement Logic: Determine next target based on direction
                direction = bus_directions[bus.id]
                
                # If moving forward, target is closest_idx + 1 (if we haven't reached closest_idx yet)
                # But actually, if we are NOT at a stop, we are BETWEEN stops.
                # Let's find the logical "next" stop based on our last known stop.
                
                # Simplified: move toward the stop that follows our direction
                target_idx = closest_idx + direction
                
                # Clamp target_idx
                if target_idx >= num_stops: target_idx = num_stops - 1
                if target_idx < 0: target_idx = 0
                
                target_stop = stops[target_idx]
                prev_stop = stops[closest_idx]
                
                # Calculate step to finish in 30s (10 ticks) with slight variation
                import random
                total_leg_dist = math.sqrt((target_stop.latitude - prev_stop.latitude)**2 + (target_stop.longitude - prev_stop.longitude)**2)
                speed_factor = random.uniform(0.8, 1.2) # Randomize speed by +/- 20%
                step = (total_leg_dist / 10.0) * speed_factor
                
                # If the leg distance is 0 (same stop), just move to next
                if step == 0: step = 0.0005 

                angle = math.atan2(target_stop.latitude - loc.latitude, target_stop.longitude - loc.longitude)
                new_lat = loc.latitude + math.sin(angle) * step
                new_lng = loc.longitude + math.cos(angle) * step
                
                # Prevent overshooting
                dist_to_target = math.sqrt((target_stop.latitude - new_lat)**2 + (target_stop.longitude - new_lng)**2)
                if dist_to_target < step:
                    new_lat = target_stop.latitude
                    new_lng = target_stop.longitude

                db.add(LocationModel(bus_id=bus.id, latitude=new_lat, longitude=new_lng))
                db.commit()

        except Exception as e:
            print(f"Simulation Error: {e}")
        finally:
            db.close()
        time.sleep(3)

@app.on_event("startup")
def startup():
    print("Application Startup: Starting simulation thread...")
    threading.Thread(target=simulate_buses, daemon=True).start()
    create_admin()