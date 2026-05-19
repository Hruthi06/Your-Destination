# Your-Destination: Real-Time Bus Tracking App

**Your-Destination** is a real-time city bus tracking application featuring an interactive live simulation, user route favorites, and an admin management dashboard. The interface features a premium dark-themed glassmorphism design.

---

## 🚀 Key Features

* **Interactive Live Map**: Real-time visualization of bus movement along snapped routes powered by Leaflet.js.
* **Continuous Bus Simulation**: Background simulation engine dynamically moving active buses along route stops.
* **User Dashboard**:
  * Real-time search for active routes and bus status.
  * Save favorite routes for quick access.
* **Admin Control Panel**:
  * Track active vehicles and user statuses.
  * Manage routes, registered buses, and system configurations.
* **Security & Authentication**: JWT-token based security, password hashing, and user role management.

---

## 🛠️ Tech Stack

* **Backend**: Python, FastAPI
* **Database**: MySQL, SQLAlchemy (ORM)
* **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism Design), JavaScript
* **Mapping API**: Leaflet.js

---

## 📂 Project Structure

```text
Your-Destination/
│
├── app/                        # Backend Application Core
│   ├── config/                 # Security & Session Configurations
│   ├── models/                 # SQLAlchemy DB Models (Bus, Route, Stop, User)
│   ├── routes/                 # FastAPI Router Endpoints (Admin, Auth, Map, etc.)
│   ├── schemas/                # Pydantic schemas for data validation
│   ├── services/               # Internal business logic and helpers
│   ├── database.py             # Database engine setup
│   └── main.py                 # Application Entry Point & Simulation Engine
│
├── assets/                     # Frontend Static Assets (CSS, Logos)
│
├── venv/                       # Python Virtual Environment (ignored in git)
├── .env                        # Local Environment Config (ignored in git)
├── .gitignore                  # Git Ignore configuration
├── migrate.py                  # Database Schema Migration Script
├── seed_tumkur.py              # Seeding script for Tumkur city routes & stops
├── run_simulation.py           # Standalone continuous simulation script
│
├── index.html / login.html     # Client Webpages
├── admin.html / user.html      # Admin & User Dashboards
└── map.html                    # Real-time Tracking Interface
```

---

## 💻 Local Setup & Execution

### 1. Database Configuration
1. Start your local MySQL Server.
2. Create the target database:
   ```sql
   CREATE DATABASE your_destination;
   ```
3. Create a `.env` file in the root directory and add your database URL:
   ```env
   DATABASE_URL=mysql+pymysql://root:YourNewPasswordHere@localhost:3306/your_destination
   SECRET_KEY=your_secret_key
   ```
   *(Ensure special characters in the password are URL-encoded).*

### 2. Python Environment Setup
1. Activate the Python virtual environment:
   * **PowerShell**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * **Command Prompt**:
     ```cmd
     .\venv\Scripts\activate.bat
     ```
2. Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Setup Database Schema & Seed Data
1. Run migrations to create and modify tables:
   ```bash
   python migrate.py
   ```
2. Seed the database with Tumkur city routes, stops, and mock bus lines:
   ```bash
   python seed_tumkur.py
   ```

### 4. Start the Application Server
Run the FastAPI web server:
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## 🔑 Access Credentials

* **User Dashboard / Live Tracking**: `http://127.0.0.1:8000/user`
* **Admin Login**: `http://127.0.0.1:8000/admin/login`
  * **Email**: `admin@admin.com`
  * **Password**: `admin123`
* **User Login**: `http://127.0.0.1:8000/login`
