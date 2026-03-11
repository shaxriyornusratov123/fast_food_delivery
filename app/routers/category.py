from fastapi import HTTPException, APIRouter
from app.database import db_dep
from sqlalchemy import select
from app.models import Category
from app.schemas.category import Create_cat, Update_cat, Response_cat, Delete_cat

router = APIRouter(prefix="/category", tags=["Category"] )

@router.get("/Categories", response_model= Response_cat)
async def cats(db:db_dep ):
    stmt = select(Category).order_by(Category.name)
    res = db.execute(stmt).scalars().all()
    return res


@router.post("/Create_category")
async def create_cat(db:db_dep, create_request:Create_cat ):
    stmt = select(Category).where(Category.name == create_request.name)
    
    if stmt == False :
        raise HTTPException(status_code=201, detail="category exist") # if i`m not mistaken `
    new_cat = Category(
        id = create_request.id,
        name = create_request.name
    )
    db.add(new_cat)
    db.commit()
    return new_cat

@router.put("/Update_category")
async def update_cat(db:db_dep, update_request:Update_cat):
    stmt = select(Category).where(Category.name == update_request.name)
    res = db.execute(stmt)
    categ = res.scalars().first()

    if not categ:
        raise HTTPException(status_code=404, detail="Category not found")
    
    categ.name == update_request.name

    db.commit()
    db.refresh(categ)
    return categ


@router.delete("/Delete_category", status_code=204)
async def delete_cat(db:db_dep, delete_request:Delete_cat):
    stmt = select(Category).where(Category.name == delete_request.name)
    res = db.execute(stmt)
    categ = res.scalars().first()

    if not categ:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(categ)
    db.commit()
    return None