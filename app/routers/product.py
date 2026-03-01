from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Product
from app.database import db_dep
from app.schemas.product import (
    ProductListResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
)
from app.dependencies import current_user_dep


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{product_id}", response_model=ProductListResponse)
async def get_product(session: db_dep, product_id: int):
    stmt = select(Product).where(Product.id == product_id)
    res = session.execute(stmt)
    product = res.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return product


@router.get("/{name}", response_model=ProductListResponse)
async def get_product(session: db_dep, name: str):
    stmt = select(Product).where(Product.name.ilike(f"%{name}%"))
    res = session.execute(stmt)
    product = res.scalars().all()

    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return product


@router.post("/create")
async def create_product(
    session: db_dep, create_data: ProductCreateRequest, current_user: current_user_dep
):

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to create product")

    product = Product(
        subcategory_id=create_data.subcategory_id,
        image_id=create_data.image_id,
        name=create_data.name,
        description=create_data.description,
        price=create_data.description,
    )

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@router.put("/{product_id}")
async def update_product(
    session: db_dep,
    product_id: int,
    update_data: ProductUpdateRequest,
    current_user: current_user_dep,
):

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to update product")

    stmt = select(Product).where(Product.id == product_id)
    res = session.execute(stmt)
    product = res.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if update_data.subcategory_id:
        product.subcategory_id = update_data.subcategory_id
    if update_data.image_id:
        product.image_id = update_data.image_id
    if product.name:
        product.name = update_data.name
    if product.description:
        product.description = update_data.description
    if product.price:
        product.price = update_data.price

    session.commit()
    session.refresh(product)

    return product


@router.delete("/{prodduct_id}/")
async def delete_product(
    session: db_dep, product_id: int, current_user: current_user_dep
):

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to delete product")

    stmt = select(Product).where(Product.id == product_id)
    res = session.execute(stmt)
    product = res.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()

