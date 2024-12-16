from django.shortcuts import render

# from django.http import HttpResponse


def order(request):
    pass


def failed(request):
    return render(request, "order/order_failed.html")


def successful(request):
    return render(request, "order/order_successful.html")
