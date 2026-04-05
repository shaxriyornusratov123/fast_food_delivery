from sqlalchemy.orm import joinedload
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models import Cart, CartItem, Product
from app.schemas.cart import AddToCartRequest, UpdateCartItemRequest
from app.database import db_dep


async def load_cart(session: db_dep, cart_id: int) -> Cart:
    stmt = (
        select(Cart)
        .options(joinedload(Cart.cart_items).joinedload(CartItem.product))
        .where(Cart.id == cart_id)
    )
    return session.execute(stmt).scalars().first()


async def get_product(session: db_dep, product_id: int) -> Product:
    stmt = select(Product).where(Product.id == product_id)
    product = session.execute(stmt).scalars().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id={product_id} not found",
        )
    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product '{product.name}' is not available",
        )

    return product


async def recalculate_total(cart: Cart) -> None:
    cart.total_price = round(
        sum(item.price * item.quantity for item in cart.cart_items), 2
    )


async def get_or_create_cart(session: db_dep, user_id: int):
    stmt = (
        select(Cart)
        .options(joinedload(Cart.cart_items).joinedload(CartItem.product))
        .where(Cart.user_id == user_id)
    )

    cart = session.execute(stmt).scalars().first()

    if cart is None:
        cart = Cart(user_id=user_id, total_price=0)
        session.add(cart)
        session.commit()
        session.refresh(cart)

    return load_cart(session, cart.id)


async def add_item(session: db_dep, user_id: int, create_data: AddToCartRequest):
    product = get_product(session, create_data.product_id)
    cart = get_or_create_cart(session, user_id)

    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, CartItem.product_id == product.id
    )
    existing = session.execute(stmt).scalars().first()

    if existing:
        new_qty = existing.quantity + create_data.quantity
        if new_qty > 99:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Maximum 99 units per product allowed",
            )
        existing.quantity = new_qty
        cart_item = existing
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=create_data.quantity,
            price=product.price,
        )
        session.add(cart_item)
        session.flush()

    recalculate_total(cart)
    session.commit()

    cart = load_cart(session, cart.id)

    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, CartItem.product_id == product.id
    )
    cart_item = session.execute(stmt).scalars().first()

    return cart_item, cart


async def update_item(
    session: db_dep, user_id: int, item_id: int, create_data: UpdateCartItemRequest
):
    cart = get_or_create_cart(session, user_id)

    stmt = select(CartItem).where(CartItem.cart_id == cart.id, CartItem.id == item_id)
    cart_item = session.execute(stmt).scalars().first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if create_data.quantity == 0:
        session.delete(cart_item)
    else:
        cart_item.quantity = create_data.quantity

    session.flush()
    recalculate_total(cart)
    session.commit()

    return load_cart(session, cart.id)


def clear_cart_after_order(session: db_dep, user_id: int):
    cart = get_or_create_cart(session, user_id)

    stmt = select(CartItem).where(CartItem.cart_id == cart.id)
    items = session.execute(stmt).scalars().all()

    for item in items:
        session.delete(item)

    cart.total_price = 0
    session.commit()

    return load_cart(session, cart.id)
