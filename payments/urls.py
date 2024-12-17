from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("", views.payment_home, name="payment_home"),
    path("payment", views.linepay_payment, name="linepay_payment"),
    path("confirm", views.linepay_confirm, name="linepay_confirm"),
    path("cancel", views.linepay_cancel, name="linepay_cancel"),
    path("request", views.request, name="request"),
]


# payment/urls.py

from django.contrib import admin
from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("request", views.request, name="request"),
]
