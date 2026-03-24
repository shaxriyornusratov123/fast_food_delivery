from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Discount
from app.database import db_dep
from app.schemas.discount import DiscountCreateRequest
from app.dependencies import current_user_dep

router = APIRouter(prefix="/discounts", tags=["Discounts"])


@router.post("/create")
async def create_discount(
    session: db_dep, create_data: DiscountCreateRequest, current_user: current_user_dep
):
    discount = Discount(
        name=create_data.name,
        discount_type=create_data.discount_type,
        value=create_data.value,
        start_date=create_data.start_date,
        end_date=create_data.end_date,
        is_active=create_data.is_active,
    )

    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")

    session.add(discount)
    session.commit()
    session.refresh(discount)

    return {"message": "Discount successfully created"}
