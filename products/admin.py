from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Product, Favorite, ComparisonItem, Order, OrderItem
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "id",
        "email",
        "display_name",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "is_active",
        "is_staff",
    )

    search_fields = (
        "email",
        "display_name",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("個人資料", {
            "fields": (
                "display_name",
                "first_name",
                "last_name",
            )
        }),
        ("權限", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("重要日期", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "display_name",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "status",
    )

    search_fields = (
        "id",
        "name",
        "category",
    )

    list_filter = (
        "category",
        "status",
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "created_at",
    )

    search_fields = (
        "user__email",
        "product__name",
    )

@admin.register(ComparisonItem)
class ComparisonItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__email",
        "product__name",
        "product__id",
    )

    ordering = (
        "-created_at",
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "user__email",
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "unit_price",
    )