from fastapi import APIRouter
from sqlalchemy import select

from app.models import Order
from app.database import db_dep
from app.schemas.order import OrderListResponse, OrederCreateRequest
from app.dependencies import current_user_dep

router = APIRouter(prefix="/orders", tags=["/Orders"])


@router.get("/list/")
async def get_orders(session: db_dep):
    # TODO: list with search, filter
    pass


@router.get("/{order_id}", response_model=OrderListResponse)
async def get_order(session: db_dep, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    res = session.execute(stmt)
    product = res.scalars().first()

    return product


@router.post("/create")
async def create_order(
    session: db_dep, create_data: OrederCreateRequest, current_user: current_user_dep
):
    # TODO: where is order items?
    order = Order(
        user_id=create_data.user_id,
        address_id=create_data.address_id,
        promocode_id=create_data.promocode_id,
        branch_id=create_data.branch_id,
        total_price=create_data.total_price,
    )

    session.add(order)
    session.commit()
    session.refresh(order)

    return order
