from pydantic import BaseModel


class ProductListResponse(BaseModel):
    id: int
    subcategory_id: int
    image_id: int
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
    subcategory_id: int
    image_id: int
    name: str
    description: str
    price: int


class ProductUpdateRequest(BaseModel):
    subcategory_id: int
    image_id: int
    name: str
    description: str
    price: int
    is_active: bool
