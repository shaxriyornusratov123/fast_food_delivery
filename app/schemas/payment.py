from pydantic import BaseModel
from enum import StrEnum


class PaymentCreateRequest(BaseModel):
    order_id: int
    payment_type: str
    amount: int


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentCreateResponse(BaseModel):
    order_id: int
    payment_type: str
    amount: int
    status: PaymentStatus
    paid_at: bool
