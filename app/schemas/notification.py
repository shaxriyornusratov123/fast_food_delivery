from pydantic_settings import BaseSettings


class Create_Notif_req(BaseSettings):
    name: str | None = None
    title: str | None = None
    message: str | None = None
    is_read: bool | None = None
    is_send_to_all: bool | None = None


class Delete_Notif_req(BaseSettings):
    title: str


class Update_Notif_req(BaseSettings):
    name: str | None = None
    title: str | None = None
    message: str | None = None


from pydantic import BaseModel
from typing import Optional

class NotificationCreateRequest(BaseModel):
    user_id: Optional[int] = None  # None если отправляем всем
    title: str
    message: str
    image_id: Optional[int] = None
    is_sent_to_all: bool = False

class NotificationReadResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    image_id: Optional[int]
    is_read: bool
    is_sent_to_all: bool
