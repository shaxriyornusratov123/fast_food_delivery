from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Order, Product, OrderItem
from app.database import db_dep
from app.schemas.order import OrderListResponse, OrederCreateRequest
from app.dependencies import current_user_dep

router = APIRouter(prefix="/orders", tags=["Orders"])


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
    total = 0
    order = Order(user_id=current_user.id)

    session.add(order)
    session.flush()

    for item in create_data.items:
        product = session.get(Product, item.product_id)

        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product with id {item.product_id} not found!"
            )

        total += product.price * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            prpoduct_id=product.id,
            quantity=item.quantity,
            price=product.price,
        )

        session.add(order_item)

    order.total_price = total

    session.commit()
    session.refresh(order)

    return order
