from pydantic import BaseModel
from typing import Optional


class NotificationCreateRequest(BaseModel):
    user_id: Optional[int] = None
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
