from pydantic_settings import BaseSettings

class Create_Notif_req(BaseSettings):
    name : str | None = None
    title : str | None = None
    message : str | None = None
    is_read : bool | None = None
    is_send_to_all : bool | None = None

class Delete_Notif_req(BaseSettings):
    title : str 


class Update_Notif_req(BaseSettings):
    name: str | None = None
    title : str | None = None
    message : str | None = None