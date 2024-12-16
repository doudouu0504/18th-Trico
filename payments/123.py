from datetime import datetime


from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

import secrets
import json
import hmac
import hashlib
import base64
import requests


def line_pay_request(request):

    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.get(order_id=order_id)

        order.confirm()

        package_id = order.pk
        url = f"{env('LINE_SANDBOX_URL')}{env('LINE_REQUEST_URL')}"

        products = [
            {
                "id": "1",
                "name": "甜點",
                "quantity": 1,
                "price": order.total,
            }
        ]
        amount = sum([product["quantity"] * product["price"] for product in products])

        payload = {
            "amount": amount,
            "currency": "TWD",
            "orderId": order_id,
            "packages": [
                {
                    "id": package_id,
                    "amount": amount,
                    "products": products,
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"{env("DOMAIN")}/orders/line_pay_confirm",
                "cancelUrl": f"{env("DOMAIN")}/orders/line_pay_cancel",
            },
        }

        LINE_PAY_URI = env("LINE_SIGNATURE_REQUEST_URI")
        headers = create_line_pay_headers(payload, LINE_PAY_URI)
        body = json.dumps(payload)
        response = requests.post(url, headers=headers, data=body)

        if response.status_code == 200:
            data = response.json()
            if data["returnCode"] == "0000":
                return redirect(data["info"]["paymentUrl"]["web"])
            else:
                print(data["returnMessage"])
                return render(request, "orders/line_pay_checkout.html")
        else:
            print(f"Error: {response.status_code}")
            return render(request, "orders/line_pay_checkout.html")

    else:
        return render(request, "orders/line_pay_checkout.html")


def create_line_pay_headers(body, uri):

    nonce = secrets.token_hex(16)
    LINE_PAY_CHANNEL_SECRET = env("LINE_PAY_CHANNEL_SECRET")
    body_to_json = json.dumps(body)
    message = LINE_PAY_CHANNEL_SECRET + uri + body_to_json + nonce

    binary_message = message.encode()
    binary_LINE_PAY_CHANNEL_SECRET = LINE_PAY_CHANNEL_SECRET.encode()

    hash = hmac.new(binary_LINE_PAY_CHANNEL_SECRET, binary_message, hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": env("LINE_PAY_CHANNEL_ID"),
        "X-LINE-Authorization-Nonce": nonce,
        "X-LINE-Authorization": signature,
    }

    return headers


@csrf_exempt
def line_pay_confirm(request):
    transaction_id = request.GET.get("transactionId")
    order_id = request.GET.get("orderId")
    order = Order.objects.get(order_id=order_id)
    uri = f"{env('LINE_SANDBOX_URL')}/v3/payments/{transaction_id}/confirm"

    products = [
        {
            "id": "1",
            "name": "甜點",
            "quantity": 1,
            "price": order.total,
        }
    ]
    amount = sum([product["quantity"] * product["price"] for product in products])

    payload = {
        "amount": amount,
        "currency": "TWD",
    }

    signature_uri = f"/v3/payments/{transaction_id}/confirm"
    headers = create_line_pay_headers(payload, signature_uri)
    body = json.dumps(payload)
    response = requests.post(uri, headers=headers, data=body)

    data = response.json()
    if data["returnCode"] == "0000":
        return redirect("orders:line_pay_success", order_id=order_id)
    else:
        print(data["returnMessage"])
        return render(request, "orders/line_pay_fail.html")


def line_pay_cancel(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order.fail()
    return render(request, "orders/line_pay_cancel.html")


def line_pay_success(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order.pay()
    context = {
        "order": order,
    }

    return render(request, "orders/line_pay_success.html", context=context)
