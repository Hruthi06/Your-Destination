from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def migrate():
    with engine.connect() as conn:
        print("Starting migrations...")
        
        # Add is_blocked to users table
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_blocked BOOLEAN DEFAULT FALSE"))
            print("Added is_blocked to users table.")
        except Exception as e:
            print(f"Skipping is_blocked for users: {e}")

        # Add status to buses table
        try:
            conn.execute(text("ALTER TABLE buses ADD COLUMN status VARCHAR(20) DEFAULT 'RUNNING'"))
            print("Added status to buses table.")
        except Exception as e:
            print(f"Skipping status for buses: {e}")

        # Add route_id to buses table
        try:
            conn.execute(text("ALTER TABLE buses ADD COLUMN route_id INT, ADD FOREIGN KEY (route_id) REFERENCES routes(id)"))
            print("Added route_id to buses table.")
        except Exception as e:
            print(f"Skipping route_id for buses: {e}")

        # Create favorites table
        try:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    route_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (route_id) REFERENCES routes(id)
                )
            """))
            print("Created favorites table.")
        except Exception as e:
            print(f"Error creating favorites table: {e}")
        
        conn.commit()
        print("Migrations complete.")

if __name__ == "__main__":
    migrate()
