from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import Payment, Order
from app.dependencies import current_user_dep
from app.schemas.payment import PaymentCreateRequest, PaymentCreateResponse

router = APIRouter(prefix="/payment", tags=["Payments"])


@router.post("/create", response_model=PaymentCreateResponse)
async def create_payment(
    session: db_dep, current_user: current_user_dep, create_data: PaymentCreateRequest
):
    stmt = select(Order).where(
        Order.id == create_data.order_id, Order.user_id == current_user.id
    )
    order = session.execute(stmt).mappings().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    payment = Payment(
        order_id=create_data.order_id,
        payment_type=create_data.payment_type,
        amount=create_data.amount,
    )

    try:
        session.add(payment)
        session.commit()
        session.refresh(payment)

        return {"status": " payment successful paid"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=402, detail=f"payment declined: {e}")
