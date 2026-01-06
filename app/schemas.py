# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# =======================
# 1. USER SCHEMAS
# =======================

# Base class for shared attributes
class UserBase(BaseModel):
    username: str
    email: EmailStr 
    # EmailStr validates that the string is actually an email format (user@example.com)

# Schema for CREATING a user (Signup)
# We need the password here.
class UserCreate(UserBase):
    password: str

# Schema for RETURNING a user (Response)
# We EXCLUDE the password here for security.
class UserResponse(UserBase):
    id: int
    created_at: datetime
    # role: str = "student" (Optional, if you implemented roles)

    # Configuration class to tell Pydantic:
    # "It's okay to read data from a standard Python Object (ORM), not just a dictionary."
    class Config:
        from_attributes = True 

# =======================
# 2. COURSE SCHEMAS
# =======================

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    collection_name: str # Internal RAG collection name

class CourseResponse(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

# =======================
# 3. ENROLLMENT SCHEMAS
# =======================

class EnrollmentBase(BaseModel):
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    user_id: int
    enrolled_at: datetime
    
    # We can even nest schemas!
    # This would return the full course details inside the enrollment object
    course: CourseResponse 

    class Config:
        from_attributes = True