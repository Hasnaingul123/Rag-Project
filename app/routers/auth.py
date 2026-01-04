from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, crud

# Create the router instance
# prefix="/auth" means all URLs here will start with /auth
# tags=["Authentication"] organizes them nicely in the documentation
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Dependency Injection: This gives us a fresh database session for this request
get_db = database.get_db

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    1. Check if email already exists.
    2. If yes, throw error.
    3. If no, create user and return it.
    """
    
    # 1. Check for duplicates
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    # 2. Create the user
    return crud.create_user(db=db, user=user)