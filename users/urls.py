from django.urls import path
from .views import register, login, logout, profile, switch_client, switch_freelancer
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("switch_client/", switch_client, name="switch_client"),
    path("switch_freelancer/", switch_freelancer, name="switch_freelancer"),
    # 忘記密碼相關的路由
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url="/users/password_reset_done/",
            extra_context={
                "protocol": settings.PROTOCOL,
                "domain": settings.DEFAULT_DOMAIN,
            },
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="/users/reset_done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
