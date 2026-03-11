
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.dependencies import current_user_dep
from app.schemas.branches import Branch_create_req, Branch_update_req, Branch_delete_req
from app.models import Branches

router = APIRouter(prefix="/branches", tags=["Branches"])


@router.get("/all")
async def get_branch(db: db_dep):
    stmt = select(Branches).order_by(Branches.address)
    res = db.execute(stmt)

    return res.scalars().all()


@router.post("/create")
async def create_branch(db: db_dep, request: Branch_create_req, current_user:current_user_dep):
    stmt = select(Branches).where(Branches.address == request.address)
    res = db.execute(stmt)
    branch = res.scalars().first()
    
    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if branch:
        raise HTTPException(status_code=409, detail="Branch already exist")
    
    branch = Branches(
        address=request.address,
        working_hours=request.working_hours,
        branch_phone=request.phone,
    )

    db.add(branch)
    db.commit()
    return branch


@router.patch("/update")
async def update_branch(db: db_dep, request: Branch_update_req, current_user:current_user_dep):
    stmt = select(Branches).where(Branches.id == request.id)
    res = db.execute(stmt)
    brnch = res.scalars().first()

    if not brnch:
        raise HTTPException(status_code=404, detail="Branch not found")

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if brnch:
        brnch.id = (request.id,)
        brnch.address = (request.address,)
        brnch.branch_phone = (request.phone,)
        brnch.working_hours = request.working_hours

    db.commit()
    db.refresh(brnch)
    return brnch


@router.delete("/delete", status_code=204)
async def delete_branch(db: db_dep, request: Branch_delete_req, current_user:current_user_dep):
    stmt = select(Branches).where(Branches.address == request.address)
    res = db.execute(stmt)
    brnch = res.scalars().first()

    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not brnch:
        raise HTTPException(status_code=404, detail="Branch not found")

    db.delete(brnch)
    db.commit()
