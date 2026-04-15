from pydantic import BaseModel


class AddressCreateRequest(BaseModel):
    location_name: str
    latitude: float
    longitude: float


class AddressCreatResponse(BaseModel):
    id: int
    user_id: int
    location_name: str
    latitude: float
    longitude: float


class AddressUpdateRequest(BaseModel):
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class AddressListResponse(BaseModel):
    id: int
    location_name:str
    latitude: float
    longitude: float