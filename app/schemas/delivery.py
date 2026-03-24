from pydantic import BaseModel
from enum import StrEnum


class DeliveryStatus(StrEnum):
    TAYYORLANMOQDA = "tayyorlanmoqda"
    YETKAZIB_BERILMOQDA = "yetkazib berilmoqda"
    YETKAZIB_BERILDI = "yetkaziib berildi"


class DeliveryCreateRequest(BaseModel):
    order_id: int
    courier_id: int
    branch_id: int
    status: DeliveryStatus


class DeliveryCreateResponse(BaseModel):
    id: int
    order_id: int
    courier_id: int
    branch_id: int
    status: str
