from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegisterRequest":
        if self.password != self.password2:
            raise ValueError("passwords do not match")

        if len(self.password) < 8:
            raise ValueError("password must be at least 8 characters long")

        return self


class UserRegisterResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserProfileResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str | None = None
    email: EmailStr
    username: str | None = None
    password_hash: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    is_deleted: bool | None = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshToken(BaseModel):
    refresh_token: str
