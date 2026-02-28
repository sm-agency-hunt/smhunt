from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from src.core.config import settings
from src.core.logger import log

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
    # SQLite specific settings
    connect_args=(
        {"check_same_thread": False} 
        if "sqlite" in settings.DATABASE_URL 
        else {}
    )
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        log.error(f"Database session error: {e}")
        raise
    finally:
        db.close()


def get_db():
    """Dependency for FastAPI to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Initialize database and create tables"""
    try:
        # Import all models to ensure they are registered with Base
        # This ensures all tables are properly registered in metadata
        from src.database import models  # noqa: F401
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        log.info("Database tables created successfully")
        
    except Exception as e:
        log.error(f"Failed to initialize database: {e}")
        raise


def create_admin_user():
    """Create default admin user if it doesn't exist"""
    from src.database.models import User
    from src.core.security import get_password_hash
    
    # Create a session to check and create admin user
    db = SessionLocal()
    try:
        # Check if admin user exists
        admin_user = (
            db.query(User)
            .filter(User.email == "admin@smhunt.online")
            .first()
        )
        
        if not admin_user:
            admin_user = User(
                email="admin@smhunt.online",
                hashed_password=get_password_hash("admin123"),
                full_name="SMHunt Admin",
                is_superuser=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            log.info("Admin user created successfully")
        else:
            log.info("Admin user already exists")
    except Exception as e:
        db.rollback()
        log.error(f"Error creating admin user: {e}")
        raise
    finally:
        db.close()


def health_check():
    """Check database connectivity"""
    try:
        db = SessionLocal()
        # Simple query to test connection
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        log.error(f"Database health check failed: {e}")
        return False