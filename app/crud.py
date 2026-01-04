from sqlalchemy.orm import Session
from . import models, schemas, utils

# 1. READ: Get a user by email (Useful for checking if they already exist)
def get_user_by_email(db: Session, email: str):
    # effectively: SELECT * FROM users WHERE email = email LIMIT 1
    return db.query(models.User).filter(models.User.email == email).first()

# 2. CREATE: Register a new user
def create_user(db: Session, user: schemas.UserCreate):
    # Step A: Hash the password
    hashed_pwd = utils.get_password_hash(user.password)
    
    # Step B: Create the Database Model
    # We map the fields from the schema to the model
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd
    )
    
    # Step C: Add and Commit
    db.add(db_user)
    db.commit()
    
    # Step D: Refresh 
    # (This re-fetches the object from the DB so it has the generated ID and Created_At time)
    db.refresh(db_user)
    
    return db_user