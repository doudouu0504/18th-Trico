from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def portfolio_showcase(request):
    return render(request, "pages/portfolio_showcase.html")
