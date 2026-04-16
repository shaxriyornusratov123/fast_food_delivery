from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Delivery, User, Order
from app.schemas.delivery import (
    DeliveryUpdateRequest,
    DeliveryCreateResponse,
    OrderStatus,
)
from app.database import db_dep
from app.schemas.delivery import UpdateStatusRequest, valid_transitions


router = APIRouter(prefix="/delivery", tags=["Deliveries"])


@router.patch("/{delivery_id}/assign-courier", response_model=DeliveryCreateResponse)
async def assign_courier_to_delivery(
    session: db_dep, delivery_id: int, update_data: DeliveryUpdateRequest
):
    stmt = select(Delivery).where(Delivery.id == delivery_id)
    result = session.execute(stmt)
    delivery = result.scalars().first()

    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    if delivery.courier_id is not None:
        raise HTTPException(status_code=400, detail="Courier already assigned")

    courier_stmt = select(User).where(User.id == update_data.courier_id)
    courier_result = session.execute(courier_stmt)
    courier = courier_result.scalars().first()

    if not courier:
        raise HTTPException(status_code=404, detail="Courier not found")
    if not courier.is_courier:
        raise HTTPException(status_code=400, detail="User is not a courier")

    delivery.courier_id = update_data.courier_id
    delivery.status = update_data.status

    session.commit()
    session.refresh(delivery)
    return delivery


@router.put("/orders/{order_id}/status")
async def update_order_status(
    session: db_dep, order_id: int, request: UpdateStatusRequest
):
    stmt = select(Order).where(Order.id == order_id)
    order = session.execute(stmt).scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = OrderStatus(order.status)
    new_status = request.status

    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change status from {current_status.value} to {new_status.value}",
        )

    order.status = new_status.value

    session.commit()
    session.refresh(order)

    return {"message": "Status updated", "order": order}
