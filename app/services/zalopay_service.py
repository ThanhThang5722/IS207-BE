import hashlib
import hmac
import json
import time
import os
import requests
from datetime import datetime

# ZaloPay Sandbox Config
ZALOPAY_APP_ID = os.getenv("ZALOPAY_APP_ID", "2554")
ZALOPAY_KEY1 = os.getenv("ZALOPAY_KEY1", "sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn")
ZALOPAY_KEY2 = os.getenv("ZALOPAY_KEY2", "trMrHtvjo6myautxDUiAcYsVtaeQ8nhf")
ZALOPAY_ENDPOINT = os.getenv("ZALOPAY_ENDPOINT", "https://sb-openapi.zalopay.vn/v2")
ZALOPAY_CALLBACK_URL = os.getenv("ZALOPAY_CALLBACK_URL", "http://localhost:8000/api/v1/zalopay/callback")


def create_order(
    booking_id: int,
    amount: int,
    description: str,
    redirect_url: str = ""
) -> dict:
    """Tạo đơn hàng trên ZaloPay"""
    
    transID = int(time.time() * 1000) % 1000000
    app_trans_id = f"{datetime.now().strftime('%y%m%d')}_{transID}_{booking_id}"
    app_time = int(round(time.time() * 1000))
    
    embed_data = json.dumps({"redirecturl": redirect_url, "booking_id": booking_id}, separators=(',', ':'))
    item = json.dumps([{"itemid": str(booking_id), "itemname": description, "itemprice": amount, "itemquantity": 1}], separators=(',', ':'))
    
    # MAC = HMAC(key1, app_id|app_trans_id|app_user|amount|app_time|embed_data|item)
    raw_data = f"{ZALOPAY_APP_ID}|{app_trans_id}|booking_{booking_id}|{amount}|{app_time}|{embed_data}|{item}"
    mac = hmac.new(ZALOPAY_KEY1.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
    
    print(f"[ZaloPay] Raw data for MAC: {raw_data}")
    print(f"[ZaloPay] MAC: {mac}")
    
    order = {
        "app_id": ZALOPAY_APP_ID,
        "app_trans_id": app_trans_id,
        "app_user": f"booking_{booking_id}",
        "app_time": app_time,
        "embed_data": embed_data,
        "item": item,
        "amount": amount,
        "description": description,
        "bank_code": "",
        "mac": mac
    }

    try:
        response = requests.post(f"{ZALOPAY_ENDPOINT}/create", data=order, timeout=30)
        result = response.json()
        result["app_trans_id"] = app_trans_id
        print(f"[ZaloPay] Response: {result}")
        return result
    except Exception as e:
        print(f"[ZaloPay] Error: {str(e)}")
        return {"return_code": -1, "return_message": str(e)}


def verify_callback(data: str, mac: str) -> bool:
    """Verify callback từ ZaloPay"""
    computed_mac = hmac.new(ZALOPAY_KEY2.encode(), data.encode(), hashlib.sha256).hexdigest()
    return computed_mac == mac


def query_order(app_trans_id: str) -> dict:
    """Query trạng thái đơn hàng từ ZaloPay"""
    raw_data = f"{ZALOPAY_APP_ID}|{app_trans_id}|{ZALOPAY_KEY1}"
    mac = hmac.new(ZALOPAY_KEY1.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
    
    params = {
        "app_id": ZALOPAY_APP_ID,
        "app_trans_id": app_trans_id,
        "mac": mac
    }

    try:
        response = requests.post(f"{ZALOPAY_ENDPOINT}/query", data=params, timeout=30)
        return response.json()
    except Exception as e:
        return {"return_code": -1, "return_message": str(e)}
