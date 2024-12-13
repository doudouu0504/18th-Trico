from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def client(request):
    return render(request, "pages/client.html")


def freelancer(request):
    return render(request, "pages/freelancer.html")
