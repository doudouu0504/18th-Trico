from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders_as_client", verbose_name="")
    # 服務被刪除但訂單仍保留SET_NULL
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name="orders", verbose_name="服務", null=True,blank=True,)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="訂單日期")
    total_price = models.PositiveIntegerField(verbose_name="總金額")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending", verbose_name="訂單狀態")

    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單"

    def __str__(self):
        return f"Order #{self.id} - {self.client_user.username} - {self.service.title if self.service else 'No Service'}"
