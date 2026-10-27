from django.db import models
from django.db import models

class Product(models.Model):
    # 商品 ID，例如 tank、rover
    id = models.CharField(
        max_length=50,
        primary_key=True
    )

    # 商品名稱
    name = models.CharField(
        max_length=200
    )

    # 商品分類
    category = models.CharField(
        max_length=100
    )

    # 商品標籤
    tag = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    # 商品價格，允許尚未公布
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # 商品狀態
    status = models.CharField(
        max_length=100
    )

    # 商品描述
    desc = models.TextField(
        blank=True,
        default=''
    )

    # 商品規格，使用 JSON 儲存
    spec = models.JSONField(
        default=dict,
        blank=True
    )

    def __str__(self):
        return self.name