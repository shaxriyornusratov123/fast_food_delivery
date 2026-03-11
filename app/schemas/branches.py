from pydantic import BaseModel


class Branch_create_req(BaseModel):
    address: str
    working_hours: str
    phone: str


class Branch_update_req(BaseModel):
    id: int | None = None
    address: str | None = None
    working_hours: str | None = None
    phone: str | None = None


class Branch_delete_req(BaseModel):
    address: str
