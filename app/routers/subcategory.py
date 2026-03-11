from fastapi import HTTPException, APIRouter
from app.database import db_dep
from sqlalchemy import select
from app.models import Subcategory
from app.schemas.subcategory import Create_subcat, Update_subcat, Response_subcat, Delete_subcat

router = APIRouter(prefix="/subcategory", tags=["Subcategory"] )

@router.get("/Subcategories")
async def subcats(db:db_dep, response_model: Response_subcat):
    stmt = select(Subcategory).order_by(Subcategory.name)
    res = db.execute(stmt).scalars().all()
    return res


@router.post("/Create_subcategory")
async def create_subcat(db:db_dep, create_request:Create_subcat ):
    stmt = select(Subcategory).where(Subcategory.name == create_request.name)
    
    if stmt :
        raise HTTPException(status_code=201, detail="category exist") # if i`m not mistaken `
    new_cat = Subcategory(
        id = create_request.id,
        category_id = create_request.category_id,
        name = create_request.name
    )
    db.add(new_cat)
    db.commit()
    return new_cat

@router.put("/Update_subcategory")
async def update_subcat(db:db_dep, update_request:Update_subcat):
    stmt = select(Subcategory).where(Subcategory.name == update_request.name)
    res = db.execute(stmt)
    subcateg = res.scalars().first()

    if not subcateg:
        raise HTTPException(status_code=404, detail="Category not found")
    
    subcateg.name == update_request.name

    db.commit()
    db.refresh(subcateg)
    return subcateg


@router.delete("/Delete_subcategory", status_code=204)
async def delete_cat(db:db_dep, delete_request:Delete_subcat):
    stmt = select(Subcategory).where(Subcategory.name == delete_request.name)
    res = db.execute(stmt)
    categ = res.scalars().first()

    if not categ:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(categ)
    db.commit()
    return None 