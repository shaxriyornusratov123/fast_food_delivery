from fastapi import APIRouter, status

from app.database import db_dep
from app.dependencies import current_user_dep
from app.schemas.cart import (
    AddToCartRequest,
    AddToCartResponse,
    CartResponse,
    UpdateCartItemRequest,
)
from app.routers.service import (
    get_or_create_cart,
    add_item,
    update_item,
    clear_cart_after_order,
)

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
async def get_cart(
    db: db_dep,
    current_user: current_user_dep,
):
    return get_or_create_cart(db, current_user.id)


@router.post(
    "/items", response_model=AddToCartResponse, status_code=status.HTTP_201_CREATED
)
async def add_products_to_cart(
    create_data: AddToCartRequest,
    db: db_dep,
    current_user: current_user_dep,
):
    cart_item, cart = add_item(db, current_user.id, create_data)
    return AddToCartResponse(
        message="Продукт добавлен в корзину",
        cart_item_id=cart_item.id,
        cart=cart,
    )


@router.patch("/items/{item_id}", response_model=CartResponse)
async def update_cart_item(
    item_id: int,
    create_data: UpdateCartItemRequest,
    db: db_dep,
    current_user: current_user_dep,
):
    return update_item(db, current_user.id, item_id, create_data)


@router.delete("/items/{item_id}", response_model=CartResponse)
async def remove_cart_item(
    item_id: int,
    db: db_dep,
    current_user: current_user_dep,
):
    return update_item(db, current_user.id, item_id, UpdateCartItemRequest(quantity=0))


@router.delete("", response_model=CartResponse)
async def clear_cart(
    db: db_dep,
    current_user: current_user_dep,
):
    return clear_cart_after_order(db, current_user.id)
