from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str

class UserCreate(UserBase):
     password: str
     full_name: str  # ← Add this
     role: str
    
# ✅ ADD THIS NEW SCHEMA
class UserUpdate(BaseModel):
    role: Optional[str] = None
    is_approved: Optional[bool] = None
    full_name: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_approved: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    is_approved: bool  # ✅ Add this
    role: str  # ✅ Add this


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
