"""
Database initialization script for SMHUNT
Creates all tables and initializes required data
"""
import os
import sys
from sqlalchemy import create_engine, inspect

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import after path modification (intentional E402)
from src.database.connection import Base  # noqa: E402
from src.database import models  # noqa: F401,E402
from src.core.config import settings  # noqa: E402
from src.core.logger import log  # noqa: E402


def init_db():
    """Initialize the database with all required tables"""
    try:
        log.info("Initializing SMHUNT database...")

        # Create a fresh engine to ensure tables are created in the right place
        engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

        # Create all tables (checkfirst parameter prevents recreation)
        Base.metadata.create_all(bind=engine, checkfirst=True)

        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        log.info(f"Created tables: {tables}")
        tables_str = ', '.join(tables) if tables else 'None'
        print(f"✓ Created {len(tables)} tables: {tables_str}")

        # Close the engine
        engine.dispose()

        # Now import and call the actual initialization functions
        from src.database.connection import create_admin_user
        create_admin_user()

        log.info("Database initialized successfully!")
        print("✓ Database tables created successfully")
        print("✓ Admin user created (if not exists)")

    except Exception as e:
        log.error(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    init_db()
