from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class Role(str, Enum):
    COURIER = "COURIER"


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class UserOut(BaseModel):
    id: int
    name: str | None = None
    email: str
    username: str | None = None 
    phone: str | None = None
    role: Role | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ApplyRequest(BaseModel):
    message: str | None = None


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    status: ApplicationStatus
    message: str | None
    admin_note: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationWithUser(BaseModel):
    id: int
    status: ApplicationStatus
    created_at: datetime
    user: UserOut

    model_config = {"from_attributes": True}


class DecisionRequest(BaseModel):
    status: ApplicationStatus
    admin_note: str | None = None
