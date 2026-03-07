from .auth import auth_router
from .branches import router as branch_router
from .product import router as product_router
from .order import router as order_router
from .notification import router as notif_router
from .address import router as location_router
from .users import router as users_router
from .promocode import router as promocode_router

__all__ = [
    "auth_router",
    "product_router",
    "order_router",
    "branch_router",
    "notif_router",
    "location_router",
    "users_router",
    "promocode_router",
]
