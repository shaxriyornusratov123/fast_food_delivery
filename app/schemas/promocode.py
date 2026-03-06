from datetime import datetime

from pydantic import BaseModel

class CreatePromocodeRequest(BaseModel):
    code: str
    discount_percentage: int
    is_active: bool
    max_uses: int
    created_at: datetime

class UpdatepromocodeRequest(BaseModel):
    code: str
    discount_percentage: int
    max_uses: int
    is_active: bool


    