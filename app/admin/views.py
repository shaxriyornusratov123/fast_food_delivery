from starlette_admin.contrib.sqla import ModelView


class UserAdminView(ModelView):
    fields = [
        "id",
        "email",
        "password_hash",
        "first_name",
        "last_name",
        "is_active",
        "is_courier",
        "is_staff",
        "is_superuser",
        "deleted_email",
        "created_at",
        "updated_at",
        "is_deleted",
    ]

    exclude_fields_from_list = ["password_hash", "deleted_email", "is_deleted"]

    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "password_hash", "created_at", "updated_at"]


class OrderAdminView(ModelView):
    fields = [
        "id",
        "user_id",
        "address_id",
        "promocode_id",
        "branch_id",
        "status",
        "total_price",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_list = ["user_id", "address_id", "promocode_id", "branch_id"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = [
        "id",
        "created_at",
        "updated_at",
        "user_id",
        "address_id",
    ]


class ProductAdminView(ModelView):
    fields = ["id", "category_id", "image_id", "name", "description", "price"]

    exclude_fields_from_list = [ "description"]
    exclude_fields_from_create = ["id"]
    exclude_fields_from_edit = ["id"]


class CategoryAdminView(ModelView):
    fields = ["id", "name"]

    exclude_fields_from_create = ["id"]
    exclude_fields_from_edit = ["id"]


class SubcategoryAdminView(ModelView):
    fields = ["id", "category_id", "name"]

    exclude_fields_from_create = ["id"]
    exclude_fields_from_edit = ["id"]


class CartAdminView(ModelView):
    fields = ["id", "user_id", "total_price", "created_at", "updated_at"]

    exclude_fields_from_create = ["id", "total_price", "created_at", "updated_at"]
    exclude_fields_from_edit = [
        "id",
        "user_id",
        "total_price",
        "created_at",
        "updated_at",
    ]


class AddressAdminView(ModelView):
    fields = ["id", "user_id", "latitude", "longitude", "created_at", "updated_at"]

    exclude_fields_from_list = ["created_at", "updated_at"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = [
        "id",
        "user_id",
        "latitude",
        "longitude",
        "created_at",
        "updated_at",
    ]


class PaymentAdminView(ModelView):
    fields = [
        "id",
        "order_id",
        "amount",
        "payment_type",
        "status",
        "paid_at",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_list = ["order_id", "paymant_type", "created_at", "updated_at"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = [
        "id",
        "order_id",
        "amount",
        "payment_type",
        "created_at",
        "updated_at",
    ]


class PromocodeAdminView(ModelView):
    fields = [
        "id",
        "code",
        "discount_percentage",
        "is_active",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_list = ["created_at", "updated_at"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]


class NotificationAdminView(ModelView):
    fields = [
        "id",
        "user_id",
        "image_id",
        "title",
        "message",
        "is_read",
        "is_sent_to_all",
        "created_at",
        "updated_at",
    ]
    exclude_fields_from_list = ["user_id", "image_id", "message"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]


class LikeAdminView(ModelView):
    fields = ["id", "user_id", "product_id", "created_at", "updated_at"]

    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]


class ImageAdminView(ModelView):
    fields = ["id", "url", "created_at", "updated_at"]

    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]


class CourierAdminView(ModelView):
    fields = [
        "id",
        "branch_id",
        "first_name",
        "last_name",
        "phone",
        "vehicle_type",
        "is_active",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]
    exclude_fields_from_list = ["created_at", "updated_at"]


class BranchAdminView(ModelView):
    fields = ["id", "address", "working_hours", "branch_phone"]

    exclude_fields_from_list = ["address"]
    exclude_fields_from_create = ["id"]
    exclude_fields_from_edit = ["id"]


class DiscountAdminView(ModelView):
    fields = [
        "id",
        "name",
        "discount_type",
        "value",
        "is_active",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_list = ["created_at", "updated_at", "discount_type"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]


class DeliveryAdminView(ModelView):
    fields = [
        "id",
        "order_id",
        "courier_id",
        "branch_id",
        "status",
        "delivery_time",
        "created_at",
        "updated_at",
    ]

    exclude_fields_from_list = ["order_id", "courier_id", "created_at", "updated_at"]
    exclude_fields_from_create = ["id", "created_at", "updated_at"]
    exclude_fields_from_edit = [
        "id",
        "order_id",
        "courier_id",
        "created_at",
        "updated_at",
    ]
