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

# Token response
class Token(BaseModel):
    access_token: str
    token_type: str

# User login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Master password verification
class MasterPasswordVerify(BaseModel):
    master_password: str


# Password Response
class PasswordResponse(BaseModel):
    id: int
    service_name: str
    username: str
    url: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at:datetime

    class Config:
        from_attributes = True


# Password create
class PasswordCreate(BaseModel):
    service_name: str
    username: Optional[str] = None
    password: str
    url: Optional[str] = None
    notes: Optional[str] = None
    master_password: str

# Password update
class PasswordUpdate(BaseModel):
    service_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    master_password: str



