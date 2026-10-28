from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 使用者管理器
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("必須提供電子郵件")
        if not password:
            raise ValueError("必須提供密碼")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("超級使用者必須設定 is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("超級使用者必須設定 is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # 不使用預設 username，改用 email 登入
    username = None

    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name"]

    # 使用上面自訂的管理器
    objects = UserManager()

    def __str__(self):
        return self.email

class Product(models.Model):
    id = models.CharField(
        max_length=50,
        primary_key=True
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, blank=True, default="")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.CharField(max_length=100)
    desc = models.TextField(blank=True, default="")
    spec = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(
        "products.User",
        on_delete=models.CASCADE,
        related_name="favorite_records"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorite_records"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_favorite"
            )
        ]


class ComparisonItem(models.Model):
    user = models.ForeignKey(
        "products.User",
        on_delete=models.CASCADE,
        related_name="comparison_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comparison_items"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 同一位會員不能重複加入相同商品
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_comparison"
            )
        ]
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "待處理"
        PAID = "paid", "已付款"
        SHIPPED = "shipped", "已出貨"
        COMPLETED = "completed", "已完成"
        CANCELLED = "cancelled", "已取消"

    user = models.ForeignKey(
        "products.User",
        on_delete=models.PROTECT,
        related_name="orders"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )