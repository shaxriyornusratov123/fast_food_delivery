from fastapi import APIRouter, HTTPException


from app.models import Delivery
from app.schemas.delivery import DeliveryCreateRequest, DeliveryCreateResponse
from app.database import db_dep


router = APIRouter(prefix="/delivery", tags=["Deliveries"])


@router.post("/create", response_model=DeliveryCreateResponse)
async def create_delivery(session: db_dep, create_data: DeliveryCreateRequest):
    delivery = Delivery(
        order_id=create_data.order_id,
        courier_id=create_data.courier_id,
        branch_id=create_data.branch_id,
        status=create_data.status,
    )

    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")

    session.add(delivery)
    session.commit()
    session.refresh(delivery)

    return {"message": "buyurtmagiz 40 daqiqada yetkazib beriladi"}
