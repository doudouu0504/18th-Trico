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
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        # 接收自定義參數，判斷「專業方案」是否需要啟用必填
        self.premium_enabled = kwargs.pop("premium_enabled", False)
        super().__init__(*args, **kwargs)

        # 專業方案字段：根據 premium_enabled 決定是否必填
        if self.premium_enabled:
            self.fields["premium_title"].required = True
            self.fields["premium_description"].required = True
            self.fields["premium_price"].required = True
            self.fields["premium_delivery_time"].required = True
        else:
            self.fields["premium_title"].required = False
            self.fields["premium_description"].required = False
            self.fields["premium_price"].required = False
            self.fields["premium_delivery_time"].required = False
