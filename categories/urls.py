from django.urls import path
from .views import all, category,tag

app_name = "categories"

urlpatterns = [
    path("", all, name="all"),
    path("<int:id>/", category, name="category"),
    path("<str:tag_name>/", tag, name="tag"),
]

