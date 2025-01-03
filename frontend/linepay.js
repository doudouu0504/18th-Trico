async function fetchLinePayData(serviceId) {
    const response = await fetch(`/api/linepay_data/${serviceId}/`);
    const data = await response.json();
    return data;
}

async function initiateLinePay(plan, serviceId) {
    const linePayData = await fetchLinePayData(serviceId);
    const price = plan === "standard" ? linePayData.standard_price : linePayData.premium_price;

    const payload = {
        amount: price,
        currency: linePayData.currency,
        orderId: `order_${Date.now()}`,
        packages: [
            {
                id: `package_${Date.now()}`,
                amount: price,
                products: [
                    { id: "1", name: `Service ${serviceId}`, quantity: 1, price: price },
                ],
            },
        ],
        redirectUrls: {
            confirmUrl: "/order/successful/",
            cancelUrl: "/order/failed/",
        },
    };

    const response = await fetch("https://sandbox-api-pay.line.me/v3/payments/request", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-LINE-ChannelId": "YOUR_CHANNEL_ID",
            "X-LINE-Authorization": "YOUR_SIGNATURE",
        },
        body: JSON.stringify(payload),
    });

    const result = await response.json();
    if (result.returnCode === "0000") {
        window.location.href = result.info.paymentUrl.web; // 跳轉到支付頁面
    } else {
        alert("支付失敗: " + result.returnMessage);
    }
}
