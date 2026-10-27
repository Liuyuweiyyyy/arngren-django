from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # 後台列表顯示的欄位
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'status',
    )

    # 可以搜尋的欄位
    search_fields = (
        'id',
        'name',
        'category',
    )

    # 右側分類篩選
    list_filter = (
        'category',
        'status',
    )