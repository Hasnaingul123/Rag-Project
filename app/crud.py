from sqlalchemy.orm import Session
from . import models, schemas, utils
from typing import Optional

# 1. READ: Get a user by email
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Retrieve a user by email address."""
    return db.query(models.User).filter(models.User.email == email).first()

# 2. CREATE: Register a new user
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user with hashed password."""
    # Step A: Hash the password
    hashed_pwd = utils.get_password_hash(user.password)
    
    # Step B: Create the Database Model
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd
    )
    
    # Step C: Add and Commit
    db.add(db_user)
    db.commit()
    
    # Step D: Refresh to get ID and timestamps
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Verify email and password. 
    Note: The specific logic is also handled in auth.py's smart login, 
    but this is useful for modularity.
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not utils.verify_password(password, user.hashed_password):
        return False
    return user