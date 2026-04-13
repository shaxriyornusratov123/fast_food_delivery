from fastapi import APIRouter, status,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import db_dep
from app.dependencies import current_user_dep
from app.schemas.cart import (
    AddToCartRequest,
    AddToCartResponse,
    CartResponse,
    UpdateCartItemRequest,
)
from app.models import Cart, CartItem,Product

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post(
    "/items", response_model=AddToCartResponse, status_code=status.HTTP_201_CREATED
)
async def add_products_to_cart(
    create_data: AddToCartRequest,
    session: db_dep,
    current_user: current_user_dep,
):

    product_stmt = select(Product).where(Product.id == create_data.product_id)
    product = session.execute(product_stmt).scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    cart_stmt = select(Cart).options(selectinload(Cart.cart_items).selectinload(CartItem.product)).where(Cart.user_id == current_user.id)
    cart = session.execute(cart_stmt).scalars().first()

    if not cart:
        cart = Cart(user_id=current_user.id, total_price=0)
        session.add(cart)
        session.flush()
        # cart.cart_items = []

    stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, CartItem.product_id == product.id
    )
    existing = session.execute(stmt).scalars().first()

    if existing:
        new_qty =  create_data.quantity
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

    cart.total_price = round(
        sum(item.price * item.quantity for item in cart.cart_items), 2
    )
    session.commit()
    return AddToCartResponse(
        message="Product added to cart successfully",
        cart_item_id=cart_item.id,
        cart=cart
    )

@router.patch("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    update_data: UpdateCartItemRequest,
    session: db_dep,
    current_user: current_user_dep,
    item_id: int
):
    stmt = select(Cart).options(
    selectinload(Cart.cart_items).selectinload(CartItem.product)  
    ).where(Cart.user_id == current_user.id)
    cart = session.execute(stmt).scalars().first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")


    stmt = select(CartItem).where(CartItem.cart_id == cart.id, CartItem.id == item_id)
    cart_item = session.execute(stmt).scalars().first()  
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if update_data.quantity == 0:
        session.delete(cart_item)
        session.flush()
    else:
        cart_item.quantity = update_data.quantity
        session.flush()

    cart.total_price = round(
        sum(item.price * item.quantity for item in cart.cart_items), 2
    )
    session.commit()
    return cart


@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_cart_item(
    item_id: int,
    session: db_dep,
    current_user: current_user_dep
):
    
    stmt = select(Cart).options(
    selectinload(Cart.cart_items).selectinload(CartItem.product)  
    ).where(Cart.user_id == current_user.id)
    cart = session.execute(stmt).scalars().first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    stmt = select(CartItem).where(CartItem.cart_id == cart.id, CartItem.id == item_id)
    cart_item = session.execute(stmt).scalars().first()  
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    session.delete(cart_item)
    session.flush()
    cart.total_price = round(
        sum(item.price * item.quantity for item in cart.cart_items), 2
    )
    session.commit()
    return cart

    
@router.delete("", response_model=CartResponse)
async def clear_cart(
    session: db_dep,
    current_user: current_user_dep,
):
    stmt = select(Cart).options(
        selectinload(Cart.cart_items).selectinload(CartItem.product)
    ).where(Cart.user_id == current_user.id)
    cart = session.execute(stmt).scalars().first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    if not cart.cart_items:
        raise HTTPException(status_code=400, detail="Cart is already empty")

    for item in cart.cart_items:
        session.delete(item)
    
    session.flush()
    cart.total_price = 0
    session.commit()
    return cart