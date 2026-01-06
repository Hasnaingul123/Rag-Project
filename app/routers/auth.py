from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import schemas, database, crud, utils, models

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Dependency Injection
get_db = database.get_db

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check for duplicates (Email OR Username)
    # We check both to prevent unique constraint errors
    existing_user = db.query(models.User).filter(
        or_(models.User.email == user.email, models.User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Username or Email already registered"
        )
    
    return crud.create_user(db=db, user=user)


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Smart Login: Accepts either Username OR Email in the 'username' field.
    Returns: JWT Access Token.
    """
    # 1. Try to find user by EMAIL first
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. If not found by email, try by USERNAME
    if not user:
        user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # 3. Validate User existence and Password
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Generate JWT Token
    access_token = utils.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}