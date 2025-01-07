from django.shortcuts import render
from django.db.models import Q
from services.models import Service
from .forms import SearchForm


def search_articles(keywords):
    return Search.objects.filter(title__icontains=keywords)


def search_view(request):
    query = None
    results = []
    if "keyword" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["keyword"]
            # 過濾標題或內容中包含關鍵字的結果
            results = Service.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
    else:
        form = SearchForm()

    return render(
        request, "search.html", {"form": form, "query": query, "results": results}
    )
