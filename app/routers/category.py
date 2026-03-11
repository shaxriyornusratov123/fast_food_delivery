from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import Category
from app.schemas.catgory import CategoryCreateRequest, Response_category, Update_category, Delete_category
from app.dependencies import current_user_dep

router = APIRouter(prefix="/category", tags=["Category"] )

@router.get("/Categories")
async def cats(db:db_dep):
    stmt = select(Category).order_by(Category.name)
    res = db.execute(stmt).scalars().all()
    return res

@router.post("/create")
async def create_category(
    db : db_dep,
    create_data: CategoryCreateRequest,
    current_user: current_user_dep,
):
    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(
            status_code=403, detail="Not authorized to create a Subcategory <- why sub.."
        )

    categ = Category(name=create_data.name)
    db.add(categ)
    db.commit()
    db.refresh(categ)

    return categ


@router.put("/Update_category")
async def update_cat(
    db:db_dep, 
    update_request:Update_category, 
    current_user:current_user_dep
    ):
    stmt = select(Category).where(Category.id == update_request.id)
    res = db.execute(stmt)
    categ = res.scalars().first()

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not categ:
        raise HTTPException(status_code=404, detail="Category not found")
    
    categ.name == update_request.name

    db.commit()
    db.refresh(categ)
    return categ


@router.delete("/Delete_category", status_code=204)
async def delete_cat(db:db_dep, delete_request:Delete_category, current_user:current_user_dep):
    stmt = select(Category).where(Category.name == delete_request.name)
    res = db.execute(stmt)
    categ = res.scalars().first()

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not categ:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(categ)
    db.commit()
    return None
