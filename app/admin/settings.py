from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import (
    User,
    Product,
    Payment,
    Promocodes,
    Discount,
    Image,
    Courier,
    Delivery,
    Branches,
    Like,
    Notification,
    Address,
    Cart,
    Category,
    Subcategory,
    Order,
)

from app.admin.views import (
    UserAdminView,
    OrderAdminView,
    ProductAdminView,
    CategoryAdminView,
    SubcategoryAdminView,
    CartAdminView,
    AddressAdminView,
    PaymentAdminView,
    PromocodeAdminView,
    NotificationAdminView,
    LikeAdminView,
    ImageAdminView,
    CourierAdminView,
    BranchAdminView,
    DiscountAdminView,
    DeliveryAdminView,
)


admin = Admin(engine=engine, title="Foodify admin", base_url="/admin")

admin.add_view(UserAdminView(User, icon="fa fa-user"))
admin.add_view(OrderAdminView(Order, icon="fa fa-receipt"))
admin.add_view(ProductAdminView(Product, icon="fa fa-utensils"))
admin.add_view(CategoryAdminView(Category, icon="fa fa-folder"))
admin.add_view(SubcategoryAdminView(Subcategory, icon="fa fa-folder-open"))
admin.add_view(CartAdminView(Cart, icon="fa fa-shopping-cart"))
admin.add_view(AddressAdminView(Address, icon="fa fa-location-dot"))
admin.add_view(PaymentAdminView(Payment, icon="fa fa-money-bill"))
admin.add_view(PromocodeAdminView(Promocodes, icon="fa fa-tag"))
admin.add_view(NotificationAdminView(Notification, icon="fa fa-bell"))
admin.add_view(LikeAdminView(Like, icon="fa fa-heart"))
admin.add_view(ImageAdminView(Image, icon="fa fa-image"))
admin.add_view(CourierAdminView(Courier, icon="fa fa-truck"))
admin.add_view(BranchAdminView(Branches, icon="fa fa-store"))
admin.add_view(DiscountAdminView(Discount, icon="fa fa-percent"))
admin.add_view(DeliveryAdminView(Delivery, icon="fa fa-shipping-fast"))
