from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import Category
from app.schemas.catgory import CategoryCreateRequest,CategoryListResponse
from app.dependencies import current_user_dep

router = APIRouter(prefix="/category", tags=["Category"])



@router.get("/list/", response_model=list[CategoryListResponse])
async def get_post_list(session: db_dep):
    stmt = select(Category)
    res = session.execute(stmt)
    category = res.scalars().all()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.post("/create")
async def create_category(
    session: db_dep,
    create_data: CategoryCreateRequest,
    current_user: current_user_dep,
):
    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(
            status_code=403, detail="Not authorized to create a Subcategory"
        )

    categ = Category(name=create_data.name)
    session.add(categ)
    session.commit()
    session.refresh(categ)

    return categ
