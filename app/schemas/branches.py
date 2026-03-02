from pydantic_settings import BaseSettings

class Branch_create_req(BaseSettings):
    name: str
    address: str
    working_hours: str
    phone:str

class Branch_update_req(BaseSettings):
    #name: str | None = None
    address: str | None = None
    working_hours: str | None = None
    phone: str | None = None

class Branch_delete_req(BaseSettings):
    address: str 