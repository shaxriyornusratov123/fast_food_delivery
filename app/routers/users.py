from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from sqlalchemy import select
from pathlib import Path
import shutil

from app.dependencies import current_user_dep
from app.schemas import user
from app.schemas.user import UserProfileResponse, UserUpdateRequest
from app.database import db_dep
from app.models import Image
from app.config import settings

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserProfileResponse)
async def me(current_user: current_user_dep):
    return current_user


@router.put("/me/update/")
async def update_user(
    session: db_dep, current_user: current_user_dep, update_data: UserUpdateRequest
):

    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if update_data.email:
        current_user.email = update_data.email
    if update_data.first_name:
        current_user.first_name = update_data.first_name
    if update_data.last_name:
        current_user.last_name = update_data.last_name
    if update_data.phone:
        current_user.phone = update_data.phone

    session.commit()
    session.refresh(current_user)

    return current_user


@router.post("/me/deactivate/")
async def deactivate_user(session: db_dep, current_user: current_user_dep):
    current_user.is_active = False

    session.commit()
    session.refresh(current_user)

    return current_user
