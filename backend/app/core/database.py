import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the database connection URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine, which is the entry point to our database
engine = create_engine(DATABASE_URL)

# Each instance of SessionLocal will be a database session. 
# This is the actual class we'll use to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We will inherit from this class to create each of the ORM models.
Base = declarative_base()

# --- Database Dependency ---
def get_db():
    """
    A FastAPI dependency that provides a database session for a single request
    and ensures it's properly closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()