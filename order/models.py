from django.db import models
from django.contrib.auth.models import User
from services.models import Service
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ("credit_card", "Credit Card"),
        ("atm", "ATM"),
        ("other", "Other"),
    ]

    # 用戶和服務關聯
    client_user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="orders_as_client", 
        verbose_name="客戶",
        null=True,
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        related_name="orders", 
        verbose_name="服務", 
        null=True,
        blank=True,
    )

    # 訂單基本資訊
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="訂單日期")
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="總金額"
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="pending", 
        verbose_name="訂單狀態"
    )

    # 支付相關欄位
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default="credit_card",
        verbose_name="付款方式"
    )
    merchant_trade_no = models.CharField(
        max_length=30, 
        unique=True, 
        null=True, 
        blank=True,
        verbose_name="商店訂單編號"
    )

    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def save(self, *args, **kwargs):
        if not self.merchant_trade_no:
            self.merchant_trade_no = f"ORDER{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        service_title = self.service.title if self.service else 'No Service'
        return f"Order {self.merchant_trade_no} - {self.client_user.username} - {service_title}"