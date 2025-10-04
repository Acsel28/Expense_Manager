from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from ..models.user import UserRole
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole


class UserCreate(UserBase):
    password: str
    company_id: int
    manager_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    role: UserRole | None = None
    manager_id: int | None = None
    password: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    company_id: int
    manager_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
