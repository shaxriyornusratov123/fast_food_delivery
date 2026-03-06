from pydantic import BaseModel
from datetime import datetime


class OrderItemCreateRequest(BaseModel):
    product_id: int
    quantity: int


class OrederCreateRequest(BaseModel):
    items: list[OrderItemCreateRequest]


class OrderUpdateRequest(BaseModel):
    user_id: int
    address_id: int
    promocode_id: int
    branch_id: int
    total_price: float


class OrderListResponse(BaseModel):
    id: int
    user_id: int
    address_id: int
    promocode_id: int
    branch_id: int
    total_price: float
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 2,
                    "address_id": 3,
                    "promocode_id": 4,
                    "branch_id": 2,
                    "total_price": 137000,
                    "created_at": "2026-01-19T13:01:18.001Z",
                }
            ]
        }
    }
