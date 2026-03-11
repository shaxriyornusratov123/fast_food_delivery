from pydantic_settings import  BaseSettings
from pydantic import BaseModel

class CategoryCreateRequest(BaseModel):
    name: str

class Update_category(BaseSettings):
    id: int | None = None
    name: str | None = None

class Response_category(BaseSettings):
    id : int
    name : str

class Delete_category(BaseSettings):
    name: str