from pydantic import BaseModel

class CategoryCreateRequest(BaseModel):
    name: str

class Update_category(BaseModel):
    id: int | None = None
    name: str | None = None

class Response_category(BaseModel):
    id : int | None = None
    name : str | None = None

class Delete_category(BaseModel):
    name: str