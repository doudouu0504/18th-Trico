from django.urls import path
from .views import home, client, freelancer

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("client/", client, name="client"),
    path("freelancer/", freelancer, name="freelancer"),
]
