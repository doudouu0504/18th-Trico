from django.contrib import admin
from django.urls import path
from order import views

app_name = "order"
urlpatterns = [
    path("failed/", views.failed, name="order_failed"),
    path("successful/", views.successful, name="order_successful"),
]
