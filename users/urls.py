from django.urls import path
from .views import (
    register,
    login,
    logout,
    profile,
    switch_client,
    switch_freelancer,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    user_dashboard,
    apply_freelancer,
    switch_role,
)

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("switch_client/", switch_client, name="switch_client"),
    path("switch_freelancer/", switch_freelancer, name="switch_freelancer"),
    # 忘記密碼相關
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset_done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_done/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("", user_dashboard, name="user_dashboard"),
    path("apply", apply_freelancer, name="apply_freelancer"),
    path("switch_role", switch_role, name="switch_role")
]

