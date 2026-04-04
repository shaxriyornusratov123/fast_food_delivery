from pydantic import BaseModel
from fastapi import Form
from datetime import datetime


class ProductListResponse(BaseModel):
    id: int
    category_id: int
    image_id: int | None = None
    name: str
    description: str
    price: int
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "subcategory_id": 2,
                    "image_id": 3,
                    "description": "katta mol gushti lavash",
                    "price": 37000,
                    "is_active": "True",
                }
            ]
        }
    }


class ProductCreateRequest(BaseModel):
    category_id: int = Form()
    discount_id: int | None = None
    name: str = Form()
    description: str = Form()
    price: int = Form()


class ProductUpdateRequest(BaseModel):
    subcategory_id: int
    image_id: int
    name: str
    description: str
    price: int
    is_active: bool


class ProductCreateResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: str
    price: int
    created_at: datetime
    updated_at: datetime
