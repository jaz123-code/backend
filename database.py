from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Create tables
 # make sure models.py is imported so SQLAlchemy sees your models


# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./memory_vault.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
Base.metadata.create_all(bind=engine)




