from django.urls import path, include
from django.conf import settings
from common.views import custom_404
from django.conf.urls.static import static
from django.urls import re_path


urlpatterns = [
    path("ckeditor5/", include("django_ckeditor_5.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404

urlpatterns += [
    re_path(r"^(?!admin|users|accounts|order|services|categories|comments|api|/).*", vue404_page),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
