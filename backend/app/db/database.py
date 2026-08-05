from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.base_model import Base

# Use the application's configuration to build the database URL
SQLALCHEMY_DATABASE_URL = settings.get_database_url()

# Configure the engine with pool_pre_ping for better connection handling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
