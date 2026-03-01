from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserProfileResponse)
async def me(current_user: current_user_jwt_dep):
    return current_user


@router.post("/me/update/")
async def update_user():
    # TODO:
    pass


@router.post("/avatar/upload/")
async def upload_avatar():
    # TODO:
    pass


@router.post("/avatar/delete/")
async def delete_avatar():
    # TODO:
    pass


@router.post("/me/deactivate/")
async def deactivate_user():
    # TODO:
    pass
