from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.user.is_authenticated:
        return redirect("pages:home")

    if request.POST:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "註冊成功!歡迎登入。")
            return redirect("users:login")
        else:
            messages.error(request, "很抱歉！請確認您的密碼。")
            return redirect("users:register")

    return render(request, "users/register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("pages:home")

    if request.POST:
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login_user(request, user)
            return redirect("pages:home")
        else:
            messages.error(request, "登入失敗，請重新登入一次。")
            return redirect("users:login")
    return render(request, "users/login.html")


@require_POST
@login_required
def logout(request):
    logout_user(request)
    response = HttpResponse()
    response["HX-Redirect"] = "/"
    return response
    # return redirect("pages:home")

@login_required
def profile(request):

    if request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("users:profile")
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }

    return render(request, "users/profile.html", context)