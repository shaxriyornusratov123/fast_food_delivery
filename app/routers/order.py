from fastapi import APIRouter, HTTPException
from sqlalchemy import select 

from app.models import Order
from app.database import db_dep
from app.schemas.order import OrderListResponse, OrderUpdateRequest,OrederCreateRequest
from app.dependencies import current_user_dep

router=APIRouter(prefix="/order",tags=["/Orders"])


