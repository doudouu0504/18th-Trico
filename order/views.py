from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from services.models import Service

from datetime import datetime
from pathlib import Path
import hashlib
import hmac
import base64
import json
import uuid
import urllib.parse

# 第三方庫
import environ
import requests


# 綠界金流設定
MERCHANT_ID = "3002607"
HASH_KEY = "pwFHCqoQZGmho4w6"
HASH_IV = "EkRm7iFT261dpevs"
ECPAY_URL = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"


# 按照綠界的規範處理參數
def generate_check_mac_value(params, hash_key, hash_iv):
    sorted_params = sorted(params.items())
    raw_str = "&".join([f"{key}={value}" for key, value in sorted_params])
    raw_str = f"HashKey={hash_key}&{raw_str}&HashIV={hash_iv}"
    # 進行 URL 編碼並轉為小寫
    encoded_str = urllib.parse.quote_plus(raw_str).lower()
    # 計算 MD5 並轉為大寫
    return hashlib.md5(encoded_str.encode("utf-8")).hexdigest().upper()


# 建立訂單
@login_required
def create_order(request):
    client_user_id = request.user.id
    service_id = request.GET.get("service_id", 1)  # 預設為 1
    total_price = 1000.0  # TODO:測試金額

    order = Order.objects.create(
        client_user_id=client_user_id,
        service_id=service_id,
        total_price=total_price,
        status="Pending",
        payment_method="CreditCard",
    )

    # 綠界金流參數
    params = {
        "MerchantID": MERCHANT_ID,
        "MerchantTradeNo": order.merchant_trade_no,
        "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": int(order.total_price),
        "TradeDesc": "Payment for Order",
        "ItemName": f"Order {order.id}",
        "ReturnURL": "http://127.0.0.1:8000/order/return/",  # TODO:部署要換
        "OrderResultURL": "http://127.0.0.1:8000/order/result/",  # TODO:部署要換
        "ChoosePayment": "Credit",
    }
    params["CheckMacValue"] = generate_check_mac_value(params, HASH_KEY, HASH_IV)

    # 將參數發送到前端表單，讓用戶跳轉至綠界支付頁面
    return render(
        request, "order/payment_form.html", {"ecpay_url": ECPAY_URL, "params": params}
    )


@csrf_exempt
def ecpay_return(request):
    if request.method == "POST":
        data = request.POST.dict()
        check_mac = data.pop("CheckMacValue", None)

        if check_mac == generate_check_mac_value(data, HASH_KEY, HASH_IV):
            merchant_trade_no = data.get("MerchantTradeNo")
            order_id = int(merchant_trade_no.replace("ORDER", ""))
            order = get_object_or_404(Order, id=order_id)
            if data.get("RtnCode") == "1":  # 成功付款
                order.status = "Paid"
                order.save()
                return HttpResponse("OK")
        return HttpResponse("CheckMacValue Failed")


@csrf_exempt
def ecpay_result(request):
    return render(request, "order/order_successful.html")


def order(request):
    pass


def failed(request):
    return render(request, "order/order_failed.html")


def successful(request):
    return render(request, "order/order_successful.html")




def payment_form_select(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    selected_plan = request.GET.get("plan")  

     # 初始表單數據
    initial_data = {
        "selected_plan": selected_plan,
        "payment_method": None,  
    }

    if request.method == "POST":
        form = OrderForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_user = request.user
            order.service = service
            # 設置總金額根據選擇的方案
            if form.cleaned_data["selected_plan"] == "standard":
                order.total_price = service.standard_price
            elif form.cleaned_data["selected_plan"] == "premium":
                order.total_price = service.premium_price
            else:
                # 如果方案不正確，返回表單錯誤
                form.add_error("selected_plan", "Invalid plan selected.")
                return render(
                    request,
                    "order/payment_form_select.html",
                    {"form": form, "service": service},
                )

            order.save()
            return redirect("order:successful", order_id=order.id)
    else:
        form = OrderForm(initial=initial_data)

    return render(
        request,
        "order/payment_form_select.html",
        {"form": form, "service": service, "selected_plan": selected_plan},
    )





# Linepay
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()

def create_headers(body, uri):
    channel_id = env('LINE_CHANNEL_ID')
    secret_key = env('LINE_CHANNEL_SECRET_KEY')

    nonce = str(uuid.uuid4())
    
    body_to_json = json.dumps(body)

    message = secret_key + uri + body_to_json + nonce

    binary_message = message.encode()
    binary_secret_key = secret_key.encode()

    hash = hmac.new(binary_secret_key, binary_message, hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId":channel_id,
        "X-LINE-ChannelSecret":secret_key,
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }
    return headers



def request_payment(request):
    if request.method == "POST":

        # 設定訂單與付款資訊
        order_id = f"order_{str(uuid.uuid4())}"
        package_id = f"package_{str(uuid.uuid4())}"

        #商品資訊
        payload = {
            'amount': 500,
            'currency': 'TWD',
            'orderId': order_id,
            'packages': [{
                'id': package_id,
                'amount': 500,
                'products': [{
                    'id': '1',
                    'name': '為你自己學 Python',
                    'quantity': 1,
                    'price': 500,
                }]
            }],
            'redirectUrls': {
                'confirmUrl': f"https://{env('HOSTNAME')}/order/successful",
                'cancelUrl': f"https://{env('HOSTNAME')}/order/failed",
            }
        }

    # 發送 API 請求
        uri = env('LINE_REQUEST_URL')
        headers = create_headers(payload, uri)
        url = f"{env('LINE_SANDBOX_URL')}{uri}"
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 根據狀態，處理回應
        if response.status_code == 200:
            data = response.json()
            if data['returnCode'] == '0000':
                return redirect(data['info']['paymentUrl']['web'])
            else:
                return render(request, "order/order_failed.html", {"message": data['returnMessage']})
        else:
            return render(request, "order/order_failed.html", {"message": f"Error: {response.status_code}"})

    return render(request, "order/linepay_test.html")