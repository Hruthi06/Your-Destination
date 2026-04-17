from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models import bus as bus_model
from app.models import route as route_model
from app.services.auth_service import hash_password
from app.routes import auth, bus, route

# ✅ Step 1: Create all tables in the database
Base.metadata.create_all(bind=engine)

# ✅ Step 2: Create the FastAPI app
app = FastAPI()

# ✅ Step 3: Register all routers AFTER app is created
app.include_router(auth.router)
app.include_router(bus.router)
app.include_router(route.router)

@app.get("/")
def home():
    return {"message": "Your Destination API is running 🚀"}

def create_admin():
    db = SessionLocal()

    admin = db.query(User).filter(User.email == "admin@admin.com").first()

    if not admin:
        new_admin = User(
            name="Admin",
            email="admin@admin.com",
            password=hash_password("admin123"),
            role="ADMIN"
        )
        db.add(new_admin)
        db.commit()
        print("✅ Admin created")
    else:
        print("⚠️ Admin already exists")

    db.close()

create_admin()