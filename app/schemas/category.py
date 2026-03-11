from pydantic_settings import BaseSettings

class Create_cat(BaseSettings):
    id : int # xato yondashuv
    name : str 

class Update_cat(BaseSettings):
    name: str | None = None

class Response_cat(BaseSettings):
    id : int
    name : str

class Delete_cat(BaseSettings):
    name: str