from pydantic_settings import BaseSettings

class Create_subcat(BaseSettings):
    id : int # xato yondashuv
    category_id: int
    name : str 

class Update_subcat(BaseSettings):
    category_id: int
    name: str | None = None

class Response_subcat(BaseSettings):
    id : int
    category_id: int
    name : str

class Delete_subcat(BaseSettings):
    name: str