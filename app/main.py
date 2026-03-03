from fastapi import FastAPI

from app.routers import auth_router, product_router, order_router,branch_router
from app.admin.settings import admin


app = FastAPI(
    title="Foodify delivery service",
    description="Foodify - fast foof delivevery service inspired from Oqtepa and Evos, built in FatsAPI",
)

app.include_router(auth_router)
app.include_router(branch_router)
app.include_router(product_router)
app.include_router(order_router)

admin.mount_to(app=app)
