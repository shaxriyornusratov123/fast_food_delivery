from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select

from app.database import db_dep
from app.schemas.branches import Branch_create_req, Branch_update_req, Branch_delete_req
from app.models import Branches

router = APIRouter(prefix="/branches", tags=["Branches"])

@router.get("/all")
async def get_branch(db:db_dep):
    stmt = select(Branches).order_by(Branches.address)
    res = db.execute(stmt)

    return res.scalars().all()


@router.post("/create")
async def create_branch(db:db_dep, request:Branch_create_req):
    branch = Branches(
        address=request.address,
        working_hours= request.working_hours,
        branch_phone= request.phone)
    
    db.add(branch)
    db.commit()
    return branch

@router.put("/update")
async def update_branch(db:db_dep, request:Branch_update_req):
    stmt = select(Branches).where(Branches.id==request.id)
    res = db.execute(stmt)
    brnch = res.scalars().first()

    if not brnch:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    if brnch:
        brnch.address = request.address,
        brnch.branch_phone = request.phone,
        brnch.working_hours = request.working_hours

    db.commit()
    db.refresh(brnch)
    return brnch


@router.delete("/delete", status_code=204)
async def delete_branch(db:db_dep, request:Branch_delete_req):
    stmt = select(Branches).where(Branches.address == request.address)
    res = db.select(stmt)
    brnch = db.scalars(res).first()

    if not brnch:
        raise HTTPException(status_code=404, detail="Branch not found")
       
    db.delete(brnch)
    db.commit()
