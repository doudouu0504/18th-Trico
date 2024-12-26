from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "title",
            "description",
            "photo",
            "category",
            "standard_title",
            "standard_description",
            "standard_price",
            "standard_delivery_time",
            "premium_title",
            "premium_description",
            "premium_price",
            "premium_delivery_time",
        ]