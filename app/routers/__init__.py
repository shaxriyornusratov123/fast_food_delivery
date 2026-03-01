from .auth import auth_router
from .product import router as product_router
from .order import router as order_router

__all__ = ["auth_router", "product_router", "order_router"]
