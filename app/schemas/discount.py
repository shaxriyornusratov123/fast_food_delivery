from pydantic import BaseModel
from datetime import datetime


class DiscountCreateRequest(BaseModel):
    name: str
    discount_type: str
    value: str
    start_date: datetime
    end_date: datetime
    is_active: bool


class DiscountCreateResponse(BaseModel):
    id: int
    name: str | None
    discount_type: str
    value: float
    start_date: datetime
    end_date: datetime
    is_active: bool
    created_at: datetime
