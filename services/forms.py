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
        # 获取额外参数
        self.premium_enabled = kwargs.pop("premium_enabled", False)  # 从 kwargs 提取参数
        super().__init__(*args, **kwargs)

        # 动态设置专业方案字段是否必填
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
