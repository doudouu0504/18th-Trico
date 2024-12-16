from django.urls import path
from .views import register, login, logout, profile, switch_client, switch_freelancer

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("switch_client/", switch_client, name="switch_client"),
    path("switch_freelancer/", switch_freelancer, name="switch_freelancer"),
]
