from fastapi import HTTPException, APIRouter
from sqlalchemy import select

from app.database import db_dep
from app.models import Notification
from app.dependencies import current_user_dep
from app.schemas.notification import (
    Create_Notif_req,
    Delete_Notif_req,
    Update_Notif_req,
)


router = APIRouter(prefix="/notif", tags=["Notification"])


@router.get("/get")
async def get_notif(db: db_dep):
    stmt = select(Notification).order_by(Notification.title)
    res = db.execute(stmt)
    notif = res.scalars().all()

    return notif


@router.post("/create")
async def create_notif(db: db_dep, request: Create_Notif_req,current_user:current_user_dep ):
    stmt = select(Notification).where(Notification.title == request.title)
    res = db.execute(stmt)
    notif = res.scalars().first()

    
    if notif :
        raise HTTPException(status_code=409, detail="already exist")
    
    
    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    notif = Notification(
        title=request.title,
        message=request.message,
        is_read=request.is_read,
        is_sent_to_all=request.is_send_to_all,
    )
    
    db.add(notif)
    db.commit()

    return notif


@router.patch("/update")
async def update_notif(db: db_dep, request: Update_Notif_req, current_user:current_user_dep):
    stmt = select(Notification).where(Notification.name == request.name)
    res = db.execute(stmt)
    notif = res.scalars().first()

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif = Notification(
        name=request.name, title=request.title, message=request.message
    )

    db.refresh(notif)
    db.commit()
    return notif


@router.delete("/delete")
async def delete_notif(db: db_dep, request: Delete_Notif_req, current_user:current_user_dep):
    stmt = select(Notification).where(Notification.title == request.title)
    res = db.execute(stmt)
    notif = res.scalars().first()

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notif)
    db.commit()
    return None
