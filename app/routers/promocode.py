from datetime import datetime 

from fastapi import APIRouter,HTTPException
from sqlalchemy import select 

from app.models import Promocodes
from app.database import db_dep
from app.schemas.promocode import CreatePromocodeRequest
from app.dependencies import current_user_dep

router=APIRouter(prefix="/promocodes",tags=["Promocodes"])

@router.post("/promocodes")
async def create_promocode(session:db_dep, create_data: CreatePromocodeRequest , current_user: current_user_dep):
    if not(current_user_dep.is_staff or current_user_dep.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to create a post  ")
    
    code=Promocodes(
        code=create_data.code,
        discount_percentage=create_data.discount_percentage,
        is_active=create_data.is_active,
        max_uses=create_data.max_uses,
        created_at=create_data.created_at
    )

    session.add(code)
    session.commit()
    session.refresh(code)

    return code  
    