from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
# def payment_form(request, id):
#     return render(request, "payments/payment_form.html", {"service_id": id})




def payment_form(request, service_id):
    # 使用 service_id 参数处理逻辑
    context = {"service_id": service_id}
    return render(request, "payments/payment_form.html", context)
