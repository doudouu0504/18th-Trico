from django.shortcuts import render, get_object_or_404
from services.models import Service, Category
from taggit.models import Tag


# Create your views here.


def all(request):
    services = Service.objects.all()
    return render(request, "categories/all.html", {"services": services})


def category(request, id):
    category = get_object_or_404(Category, id=id)
    services = Service.objects.filter(category__id=id)
    return render(
        request,
        "categories/category.html",
        {"services": services, "category": category},
    )

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    services = Service.objects.filter(tags__name__in=[tag.name])

    return render(request, "categories/tag.html", {"services": services, "tag": tag})