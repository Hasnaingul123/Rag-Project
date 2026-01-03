from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is the address of your database.
# "sqlite:///" tells the program to use SQLite.
# "./tutor.db" is the filename that will be created.
SQLALCHEMY_DATABASE_URL = "sqlite:///./tutor.db"

# 1. Create the engine (The actual connection to the file)
# connect_args={"check_same_thread": False} is needed only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2. Create a SessionLocal class
# Each time a user requests something, we create a new "Session" (interaction)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Base
# All our database models (tables) will inherit from this class
Base = declarative_base()

# Dependency: A helper function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()