from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Order, Product, OrderItem, Promocodes, Cart, CartItem
from app.database import db_dep
from app.schemas.order import OrderListResponse, OrederCreateRequest
from app.dependencies import current_user_dep


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/list")
async def list_order(session: db_dep, current_user: current_user_dep):
    stmt = (
        select(Order).where(Order.user_id == current_user.id).order_by(Order.created_at)
    )
    res = session.execute(stmt).scalars().all()

    return res


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
    order = Order(
        user_id=current_user.id,
        address_id=create_data.address_id,
        branch_id=create_data.branch_id,
    )

    session.add(order)
    session.flush()

    if create_data.cart_id is not None:
        cart_stmt = select(Cart).where(
            Cart.id == create_data.cart_id, Cart.user_id == current_user.id
        )
        cart = session.execute(cart_stmt).scalars().first()

        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        cart_items_stmt = select(CartItem).where(CartItem.cart_id == cart.id)
        cart_items = session.execute(cart_items_stmt).scalars().all()

        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        for item in cart_items:
            product = session.get(Product, item.product_id)
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with id {item.product_id} not found!",
                )

            total += item.price * item.quantity

            order_item = OrderItem(
                order_id=order.id,
                prpoduct_id=product.id,
                quantity=item.quantity,
                price=item.price,
            )
            session.add(order_item)

        for item in cart_items:
            session.delete(item)
        cart.total_price = 0

    else:
        for item in create_data.items:
            product = session.get(Product, item.product_id)

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product with id {item.product_id} not found!",
                )

            total += product.price * item.quantity

            order_item = OrderItem(
                order_id=order.id,
                prpoduct_id=product.id,
                quantity=item.quantity,
                price=product.price,
            )

            session.add(order_item)

    if create_data.promocode:
        stmt = select(Promocodes).where(
            Promocodes.code == create_data.promocode.upper()
        )
        code = session.execute(stmt).scalars().first()

        if not code:
            raise HTTPException(status_code=404, detail="Promocode not found")

        if not code.is_active:
            raise HTTPException(status_code=400, detail="Promocode is not active")

        if code.max_uses is not None and code.used_count >= code.max_uses:
            raise HTTPException(status_code=400, detail="Promocode exhausted")

        discount_amount = total * code.discount_percentage / 100
        total -= discount_amount

        code.used_count += 1
        order.promocode_id = code.id

    order.total_price = total

    session.commit()
    session.refresh(order)

    return order
