from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str


class CategoryListResponse(BaseModel):
    id: int
    name: str

    model_config = {"json_schema_extra": {"examples": [{"id": 1, "name": "Lavash"}]}}


class CategoryUpdateRequest(BaseModel):
    name: str
