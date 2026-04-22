from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class CartItemEntry(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, ge=1, le=99)


class AddToCartRequest(BaseModel):
    items: list[CartItemEntry]

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [
                    {"product_id": 3, "quantity": 2},
                    {"product_id": 4, "quantity": 2},
                ]
            }
        }
    }


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., ge=0, le=99)  # 0 = удалить



class ProductBrief(BaseModel):
    id: int
    name: str
    price: int
    description: str

    model_config = {"from_attributes": True}


class CartItemResponse(BaseModel):
    id: int
    product: ProductBrief
    quantity: int
    price: float
    subtotal: float = 0.0
    created_at: datetime

    model_config = {"from_attributes": True}

    @model_validator(mode="after")
    def compute_subtotal(self) -> "CartItemResponse":
        self.subtotal = round(self.price * self.quantity, 2)
        return self


class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float = 0.0
    items: list[CartItemResponse] = Field(alias="cart_items", default=[])
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}

    @model_validator(mode="after")
    def compute_total(self) -> "CartResponse":
        self.total_price = round(sum(item.subtotal for item in self.items), 2)
        return self



class AddToCartResponse(BaseModel):
    message: str
    cart_item_id: int
    cart: CartResponse


