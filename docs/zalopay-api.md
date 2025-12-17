# ZaloPay Payment API

## Tổng quan

API tích hợp thanh toán ZaloPay cho hệ thống booking timeshare.

**Base URL:** `/api/v1/zalopay`

---

## Flow thanh toán

```
┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│   FE    │      │   BE    │      │ ZaloPay │      │   FE    │
└────┬────┘      └────┬────┘      └────┬────┘      └────┬────┘
     │                │                │                │
     │ 1. POST /create│                │                │
     │───────────────>│                │                │
     │                │ 2. Create order│                │
     │                │───────────────>│                │
     │                │   order_url    │                │
     │                │<───────────────│                │
     │   order_url    │                │                │
     │<───────────────│                │                │
     │                │                │                │
     │ 3. Redirect to order_url        │                │
     │────────────────────────────────>│                │
     │                │                │                │
     │                │ 4. Callback    │                │
     │                │<───────────────│                │
     │                │                │                │
     │                │                │ 5. Redirect    │
     │                │                │───────────────>│
     │                │                │                │
     │ 6. POST /query │                │                │
     │───────────────>│                │                │
     │  payment status│                │                │
     │<───────────────│                │                │
```

---

## 1. Tạo đơn thanh toán

**Endpoint:** `POST /api/v1/zalopay/create`

**Mô tả:** Tạo đơn thanh toán trên ZaloPay, trả về URL để redirect user.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "booking_id": 1,
  "redirect_url": "https://your-frontend.com/payment-result"
}
```

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| booking_id | int | ✅ | ID của booking cần thanh toán |
| redirect_url | string | ❌ | URL redirect sau khi thanh toán xong |

**Response Success (200):**
```json
{
  "return_code": 1,
  "return_message": "Success",
  "order_url": "https://sb-openapi.zalopay.vn/v2/gateway/...",
  "app_trans_id": "241218_123456_1",
  "zp_trans_token": "abc123..."
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| return_code | int | 1 = thành công, khác = lỗi |
| return_message | string | Mô tả kết quả |
| order_url | string | URL redirect user đến trang thanh toán ZaloPay |
| app_trans_id | string | Mã giao dịch để query sau |
| zp_trans_token | string | Token giao dịch ZaloPay |

**Response Error:**
```json
{
  "detail": "Không tìm thấy booking hoặc booking không thuộc về bạn"
}
```

---

## 2. Query trạng thái thanh toán

**Endpoint:** `POST /api/v1/zalopay/query`

**Mô tả:** Kiểm tra trạng thái thanh toán của một giao dịch.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "app_trans_id": "241218_123456_1"
}
```

**Response Success (200):**
```json
{
  "return_code": 1,
  "return_message": "Giao dịch thành công",
  "is_processing": false,
  "amount": 2000000,
  "zp_trans_id": 240618000000123
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| return_code | int | 1 = thành công, 2 = đang xử lý, 3 = thất bại |
| return_message | string | Mô tả kết quả |
| is_processing | bool | true nếu đang xử lý |
| amount | int | Số tiền (VND) |
| zp_trans_id | int | Mã giao dịch ZaloPay |

**Return codes:**
- `1`: Thanh toán thành công
- `2`: Đang xử lý (chờ user thanh toán)
- `3`: Thanh toán thất bại

---

## 3. Callback (Webhook)

**Endpoint:** `POST /api/v1/zalopay/callback`

**Mô tả:** Webhook nhận thông báo từ ZaloPay khi thanh toán hoàn tất. **Endpoint này ZaloPay gọi, không phải FE.**

**Request Body (từ ZaloPay):**
```json
{
  "data": "{\"app_id\":2553,\"app_trans_id\":\"241218_123456_1\",\"app_time\":1734512345678,\"app_user\":\"booking_1\",\"amount\":2000000,\"embed_data\":\"{\\\"booking_id\\\":1}\",\"item\":\"[...]\",\"zp_trans_id\":240618000000123,\"server_time\":1734512345678,\"channel\":38,\"merchant_user_id\":\"user123\"}",
  "mac": "abc123...",
  "type": 1
}
```

**Response:**
```json
{
  "return_code": 1,
  "return_message": "success"
}
```

---

## Hướng dẫn tích hợp FE

### Bước 1: Gọi API tạo đơn
```javascript
const createPayment = async (bookingId) => {
  const response = await fetch('/api/v1/zalopay/create', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      booking_id: bookingId,
      redirect_url: `${window.location.origin}/payment-result`
    })
  });
  
  const data = await response.json();
  
  if (data.return_code === 1) {
    // Lưu app_trans_id để query sau
    localStorage.setItem('app_trans_id', data.app_trans_id);
    // Redirect đến ZaloPay
    window.location.href = data.order_url;
  } else {
    alert('Lỗi: ' + data.return_message);
  }
};
```

### Bước 2: Xử lý sau khi thanh toán
```javascript
// Trang /payment-result
const checkPaymentStatus = async () => {
  const appTransId = localStorage.getItem('app_trans_id');
  
  const response = await fetch('/api/v1/zalopay/query', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ app_trans_id: appTransId })
  });
  
  const data = await response.json();
  
  if (data.return_code === 1) {
    // Thanh toán thành công
    alert('Thanh toán thành công!');
    // Redirect đến trang booking history
  } else if (data.return_code === 2) {
    // Đang xử lý - có thể polling
    setTimeout(checkPaymentStatus, 3000);
  } else {
    // Thất bại
    alert('Thanh toán thất bại');
  }
};
```

---

## Test với Sandbox

Đang sử dụng môi trường sandbox ZaloPay:
- App ID: `2553`
- Endpoint: `https://sb-openapi.zalopay.vn/v2`

Để test thanh toán, sử dụng thông tin test của ZaloPay sandbox.

---

## Lưu ý

1. **Callback URL** phải được cấu hình public để ZaloPay gọi được
2. **Không tin tưởng redirect_url** - luôn verify bằng `/query` hoặc đợi callback
3. **Idempotency** - callback có thể gọi nhiều lần, BE đã xử lý check trùng
4. **Production** - cần đăng ký merchant ZaloPay và thay credentials
