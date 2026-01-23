"""
Database Configuration and Session Management
Using SQLAlchemy for ORM
Supports both SQLite (local) and PostgreSQL (Supabase)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

# Create database engine with appropriate settings
if "postgresql" in DATABASE_URL:
    # PostgreSQL/Supabase configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,
        max_overflow=20
    )
    print("🐘 Connected to PostgreSQL (Supabase)")
else:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    print("💾 Connected to SQLite (local)")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Dependency function to get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
def init_db():
    """Create all database tables"""
    from .models import user, course, schedule, semester, course_offering, completed_course, course_list  # Import all models
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
