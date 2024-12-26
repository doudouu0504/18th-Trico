from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from utils.mixins import WebPImageModelMixin


class Service(WebPImageModelMixin, models.Model):
    freelancer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="services",
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="services",
        null=True,
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to="service_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    # 新增一般方案
    standard_title = models.CharField(max_length=100)
    standard_description = models.TextField()
    standard_price = models.DecimalField(max_digits=10, decimal_places=2)
    standard_delivery_time = models.PositiveIntegerField(null=True, blank=True)

    # 新增專業方案
    premium_title = models.CharField(max_length=100, blank=True, null=True)
    premium_description = models.TextField(blank=True, null=True)
    premium_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    premium_delivery_time = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title