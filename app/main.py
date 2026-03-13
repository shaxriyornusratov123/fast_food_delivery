from fastapi import FastAPI

from app.routers import (
    auth_router,
    product_router,
    order_router,
    branch_router,
    notif_router,
    location_router,
    users_router,
    promocode_router,
    subcategory_router,
    payment_router
)
from app.admin.settings import admin

app = FastAPI(
    title="Foodify delivery service",
    description="Foodify - fast foof delivevery service inspired from Oqtepa and Evos, built in FatsAPI",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(branch_router)
app.include_router(notif_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(location_router)
app.include_router(promocode_router)
app.include_router(subcategory_router)
app.include_router(payment_router)

admin.mount_to(app=app)
