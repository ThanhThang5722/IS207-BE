# Giải thích chi tiết luồng thanh toán ZaloPay

## Tổng quan

Hệ thống tích hợp ZaloPay để xử lý thanh toán booking timeshare. Khi user thanh toán thành công, hệ thống sẽ:
- Cập nhật trạng thái booking thành "paid"
- Cập nhật trạng thái từng booking_detail thành "PAID"
- Tạo invoice cho từng phòng đã đặt

---

## Flow tổng quan

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│    FE    │     │    BE    │     │  ZaloPay │
└────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │
     │ 1. POST /create│                │
     │───────────────>│                │
     │                │ 2. Tạo order   │
     │                │───────────────>│
     │                │    order_url   │
     │                │<───────────────│
     │   order_url    │                │
     │<───────────────│                │
     │                │                │
     │ 3. Redirect ───────────────────>│
     │                │                │
     │                │ 4. Callback    │
     │                │<───────────────│
     │                │                │
     │ 5. Redirect <───────────────────│
     │                │                │
     │ 6. POST /query │                │
     │───────────────>│                │
     │  status        │                │
     │<───────────────│                │
```

---

## Chi tiết từng bước

### Bước 1: FE gọi API tạo đơn thanh toán

**Request:**
```
POST /api/v1/zalopay/create
Authorization: Bearer <token>

{
  "booking_id": 3,
  "redirect_url": "https://your-site.com/payment-result"
}
```

**Code xử lý (app/routers/customer/zalopay.py):**

```python
@router.post("/create", response_model=CreatePaymentResponse)
def create_payment(
    request: CreatePaymentRequest,
    current_account: Account = Depends(get_current_account),
    db: Session = Depends(get_db)
):
    # 1.1 Kiểm tra user có phải customer không
    if not current_account.customer:
        raise HTTPException(status_code=400, detail="Tài khoản chưa có thông tin khách hàng")
    customer_id = current_account.customer.id

    # 1.2 Tìm booking của user (phải đang pending)
    result = db.execute(
        select(Booking).filter(
            Booking.id == request.booking_id,
            Booking.customer_id == customer_id,  # Chỉ lấy booking của chính user
            Booking.status == "pending"           # Chưa thanh toán
        )
    )
    booking = result.scalar_one_or_none()

    # 1.3 Kiểm tra số tiền
    amount = int(booking.cost or 0)
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Giỏ hàng trống hoặc chưa có giá")
```

**Giải thích:**
- Lấy user từ JWT token
- Tìm booking thuộc về user và đang ở trạng thái "pending"
- Kiểm tra booking có tiền không (amount > 0)

---

### Bước 2: BE gọi ZaloPay API tạo order

**Code xử lý (app/services/zalopay_service.py):**

```python
def create_order(booking_id: int, amount: int, description: str, redirect_url: str = "") -> dict:
    
    # 2.1 Tạo mã giao dịch unique
    transID = int(time.time() * 1000) % 1000000
    app_trans_id = f"{datetime.now().strftime('%y%m%d')}_{transID}_{booking_id}"
    # Ví dụ: "251217_123456_3" = ngày 17/12/25, random 123456, booking #3
    
    # 2.2 Chuẩn bị embed_data (lưu thông tin để callback xử lý)
    embed_data = json.dumps({
        "redirecturl": redirect_url,   # URL redirect sau thanh toán
        "booking_id": booking_id       # Lưu booking_id để callback biết cập nhật booking nào
    }, separators=(',', ':'))
    
    # 2.3 Chuẩn bị item (thông tin sản phẩm)
    item = json.dumps([{
        "itemid": str(booking_id),
        "itemname": description,
        "itemprice": amount,
        "itemquantity": 1
    }], separators=(',', ':'))
    
    # 2.4 Tạo chữ ký MAC (bảo mật)
    # Format: app_id|app_trans_id|app_user|amount|app_time|embed_data|item
    raw_data = f"{ZALOPAY_APP_ID}|{app_trans_id}|booking_{booking_id}|{amount}|{app_time}|{embed_data}|{item}"
    mac = hmac.new(ZALOPAY_KEY1.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
```

**Giải thích MAC:**
- MAC (Message Authentication Code) là chữ ký số
- ZaloPay dùng MAC để verify request đến từ server của bạn
- Nếu ai đó giả mạo request, MAC sẽ không khớp → ZaloPay reject

```python
    # 2.5 Gọi API ZaloPay
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

    response = requests.post(f"{ZALOPAY_ENDPOINT}/create", data=order, timeout=30)
    result = response.json()
```

**Response từ ZaloPay:**
```json
{
  "return_code": 1,
  "return_message": "Success",
  "order_url": "https://sb-openapi.zalopay.vn/v2/gateway/...",
  "zp_trans_token": "abc123..."
}
```

---

### Bước 3: Lưu mã giao dịch và trả về FE

```python
    # Lưu app_trans_id vào DB để sau này tìm lại booking
    booking.zp_trans_id = zalo_result.get("app_trans_id")
    db.commit()

    return CreatePaymentResponse(
        return_code=zalo_result.get("return_code"),
        return_message=zalo_result.get("return_message"),
        order_url=zalo_result.get("order_url"),      # FE redirect user đến URL này
        app_trans_id=zalo_result.get("app_trans_id"),
        zp_trans_token=zalo_result.get("zp_trans_token")
    )
```

**Tại sao lưu zp_trans_id?**
- Khi ZaloPay callback, BE cần tìm đúng booking để cập nhật
- Dùng `zp_trans_id` để query booking

**FE xử lý:**
```javascript
const data = await response.json();
if (data.return_code === 1) {
  localStorage.setItem('app_trans_id', data.app_trans_id);
  window.location.href = data.order_url;  // Redirect đến ZaloPay
}
```

---

### Bước 4: User thanh toán trên ZaloPay

- User được redirect đến trang thanh toán ZaloPay
- Nhập thông tin thẻ/ví ZaloPay
- Xác nhận thanh toán
- ZaloPay xử lý giao dịch

---

### Bước 5: ZaloPay gọi Callback (Webhook)

Khi thanh toán thành công, ZaloPay gọi webhook về server của bạn.

**Request từ ZaloPay:**
```json
{
  "data": "{\"app_id\":2554,\"app_trans_id\":\"251217_123456_3\",\"amount\":2000000,\"embed_data\":\"{\\\"booking_id\\\":3}\",...}",
  "mac": "abc123...",
  "type": 1
}
```

**Code xử lý:**

```python
@router.post("/callback")
def zalopay_callback(callback: ZaloPayCallback, db: Session = Depends(get_db)):
    
    # 5.1 Verify chữ ký MAC (chống giả mạo)
    if not zalopay_service.verify_callback(callback.data, callback.mac):
        return {"return_code": -1, "return_message": "mac not equal"}
```

**Verify MAC:**
```python
def verify_callback(data: str, mac: str) -> bool:
    # Tính MAC từ data bằng KEY2
    computed_mac = hmac.new(ZALOPAY_KEY2.encode(), data.encode(), hashlib.sha256).hexdigest()
    return computed_mac == mac  # So sánh với MAC ZaloPay gửi
```

**Tại sao verify MAC?**
- Ai đó có thể giả mạo callback để hack hệ thống
- Verify MAC đảm bảo callback thực sự đến từ ZaloPay

```python
    # 5.2 Parse data và lấy booking_id
    data = json.loads(callback.data)
    embed_data = json.loads(data.get("embed_data", "{}"))
    booking_id = embed_data.get("booking_id")  # Lấy booking_id đã lưu ở bước 2.2

    # 5.3 Cập nhật booking và tạo invoice
    result = db.execute(
        select(Booking)
        .filter(Booking.id == booking_id)
        .options(selectinload(Booking.booking_details))
    )
    booking = result.scalar_one_or_none()

    if booking and booking.status == "pending":
        booking.status = "paid"  # Đánh dấu đã thanh toán
        
        # Tạo invoice cho TỪNG phòng đã đặt
        for detail in booking.booking_details:
            detail.status = "PAID"
            
            invoice = Invoice(
                customer_id=booking.customer_id,
                partner_id=1,
                booking_detail_id=detail.id,  # Gắn với từng phòng
                cost=detail.cost,
                finished_time=datetime.now(),
                payment_method="ZALOPAY"
            )
            db.add(invoice)
        
        db.commit()

    return {"return_code": 1, "return_message": "success"}
```

**Ví dụ:**
- Booking #3 có 2 phòng (booking_detail #5 và #6)
- Sau callback → tạo 2 invoices:
  - Invoice #1: booking_detail_id = 5, cost = 1,000,000
  - Invoice #2: booking_detail_id = 6, cost = 1,500,000

---

### Bước 6: FE query trạng thái (backup)

Sau khi user thanh toán xong, ZaloPay redirect về `redirect_url`. FE gọi API query để xác nhận.

**Request:**
```
POST /api/v1/zalopay/query
Authorization: Bearer <token>

{
  "app_trans_id": "251217_123456_3"
}
```

**Code xử lý:**

```python
@router.post("/query", response_model=QueryPaymentResponse)
def query_payment(request: QueryPaymentRequest, ...):
    
    # 6.1 Gọi ZaloPay API để check trạng thái
    result = zalopay_service.query_order(request.app_trans_id)
```

```python
def query_order(app_trans_id: str) -> dict:
    # Tạo MAC
    raw_data = f"{ZALOPAY_APP_ID}|{app_trans_id}|{ZALOPAY_KEY1}"
    mac = hmac.new(ZALOPAY_KEY1.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
    
    params = {
        "app_id": ZALOPAY_APP_ID,
        "app_trans_id": app_trans_id,
        "mac": mac
    }
    
    response = requests.post(f"{ZALOPAY_ENDPOINT}/query", data=params, timeout=30)
    return response.json()
```

**Response:**
```json
{
  "return_code": 1,        // 1=thành công, 2=đang xử lý, 3=thất bại
  "return_message": "Giao dịch thành công",
  "amount": 2500000,
  "zp_trans_id": 240618000000123
}
```

```python
    # 6.2 Nếu thành công, cập nhật booking (giống callback)
    if result.get("return_code") == 1:
        booking_result = db.execute(
            select(Booking)
            .filter(Booking.zp_trans_id == request.app_trans_id)
            .options(selectinload(Booking.booking_details))
        )
        booking = booking_result.scalar_one_or_none()
        
        if booking and booking.status == "pending":
            booking.status = "paid"
            # Tạo invoice cho từng detail...
```

**Tại sao cần query?**
- Callback có thể fail (network issue, server down)
- FE query để đảm bảo cập nhật được trạng thái

---

## Cấu trúc files

```
app/
├── services/
│   └── zalopay_service.py    # Gọi API ZaloPay (create, query, verify)
├── routers/customer/
│   └── zalopay.py            # 3 endpoints (create, callback, query)
├── schemas/
│   └── zalopay.py            # Request/Response schemas
└── models/
    └── booking.py            # Thêm column zp_trans_id
```

---

## Cấu hình

**Environment variables:**
```
ZALOPAY_APP_ID=2554                    # App ID từ ZaloPay
ZALOPAY_KEY1=sdngKKJmqEMzvh5QQcdD2A9XBSKUNaYn   # Key để tạo MAC
ZALOPAY_KEY2=trMrHtvjo6myautxDUiAcYsVtaeQ8nhf   # Key để verify callback
ZALOPAY_ENDPOINT=https://sb-openapi.zalopay.vn/v2  # Sandbox endpoint
ZALOPAY_CALLBACK_URL=https://your-domain.com/api/v1/zalopay/callback
```

**Production:**
- Đăng ký merchant ZaloPay để lấy credentials
- Đổi endpoint sang `https://openapi.zalopay.vn/v2`
- Cấu hình callback URL public

---

## Lưu ý bảo mật

1. **Luôn verify MAC** trong callback - không tin tưởng request không có MAC hợp lệ
2. **Check booking.status == "pending"** trước khi cập nhật - tránh xử lý trùng
3. **Lưu zp_trans_id** để trace giao dịch
4. **Không expose KEY1, KEY2** ra client
