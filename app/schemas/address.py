from pydantic import BaseModel


class AddressCreateRequest(BaseModel):
    latitude: float
    longitude: float


class AddressCreatResponse(BaseModel):
    id: int
    user_id: int
    location_name: str
    latitude: float
    longitude: float
