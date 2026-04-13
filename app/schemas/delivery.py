from pydantic import BaseModel
from enum import StrEnum


class DeliveryStatus(StrEnum):
    PENDING="pending",
    ASSIGNDE="assigned",
    DELIVERING="delivering",
    DELIVERED="delivered"
    


class DeliveryUpdateRequest(BaseModel):
    order_id: int
    courier_id: int 
    status: DeliveryStatus


class DeliveryCreateResponse(BaseModel):
    id: int
    order_id: int
    courier_id: int
    branch_id: int
    status: str


