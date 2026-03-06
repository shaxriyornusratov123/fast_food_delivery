import secrets

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.database import db_dep
from app.models import User, Cart
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse
from app.utils import hash_password, send_email, redis_client


router = APIRouter(prefix="/register", tags=["Auth"])


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(session: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = session.execute(stmt).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        email=data.email, password_hash=hash_password(data.password), is_active=False
    )

    session.add(user)
    session.flush() 

    cart = Cart(user_id=user.id)
    session.add(cart) 

    secret_code = secrets.token_hex(16)
    send_email(
        data.email, "Email confirmation", f"Your confirmation code is: {secret_code}"
    )
    redis_client.setex(secret_code, 120, user.email)

    stmt = select(User)
    existing_user = session.execute(stmt).scalars().first()

    if not existing_user:
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

    session.commit()

    return JSONResponse(
        status_code=204, content={"message": "Email confirmation sent to your email."}
    )
