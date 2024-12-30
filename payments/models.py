from django.db import models
from django.contrib.auth.models import User
from order.models import Order


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("credit_card", "Credit Card"),
        ("line_pay", "Line Pay"),
        ("ecpay", "ECPay"),  # 綠界支付
        ("blue_star", "Blue Star"),  # 藍星金流
    ]

    PAYMENT_STATUS_CHOICES = [
        ("not_paid", "Not Paid"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment", verbose_name="關聯訂單")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name="支付方式")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default="not_paid", verbose_name="付款狀態")
    payment_transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="交易流水號")
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="付款時間")

    class Meta:
        verbose_name = "支付信息"
        verbose_name_plural = "支付信息"

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.payment_status}"
