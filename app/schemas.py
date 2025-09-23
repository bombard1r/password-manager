from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User info 
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# User registeration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    master_password: str


