# Cart API Documentation

## Tổng quan

API quản lý giỏ hàng cho phép khách hàng thêm timeshare vào giỏ hàng trước khi thanh toán.

**Base URL:** `api/v1`

**Yêu cầu xác thực:** Tất cả các endpoint đều yêu cầu JWT token trong header. `customer_id` được tự động lấy từ token.

```
Authorization: Bearer <access_token>
```

---

## 1. Thêm vào giỏ hàng

**Endpoint:** `POST /api/v1/cart/items`

**Mô tả:** Thêm một item vào giỏ hàng. Customer ID tự động lấy từ token.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "offer_id": 5,
  "number_of_rooms": 2,
  "started_at": "2025-12-20T14:00:00",
  "finished_at": "2025-12-25T12:00:00"
}
```

| Field | Type | Required | Mô tả |
|-------|------|----------|-------|
| offer_id | integer | ✅ | ID của offer (gói giá phòng) |
| number_of_rooms | integer | ✅ | Số lượng phòng |
| started_at | datetime | ✅ | Ngày giờ check-in |
| finished_at | datetime | ✅ | Ngày giờ check-out |

**Response (201 Created):**
```json
{
  "message": "Item added to cart successfully"
}
```

---

## 2. Lấy giỏ hàng

**Endpoint:** `GET /api/v1/cart`

**Mô tả:** Lấy giỏ hàng của user hiện tại. Customer ID tự động lấy từ token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "customer_id": 123,
  "created_at": "2025-12-17T10:00:00",
  "status": "pending",
  "total_cost": 15000000,
  "items": [
    {
      "id": 1,
      "offer_id": 5,
      "room_type_name": "Deluxe Ocean View",
      "resort_name": "Resort ABC",
      "number_of_rooms": 2,
      "price_per_room": 2500000,
      "cost": 5000000,
      "started_at": "2025-12-20T14:00:00",
      "finished_at": "2025-12-25T12:00:00",
      "status": "pending"
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Không tìm thấy giỏ hàng"
}
```

---

## 3. Cập nhật số lượng phòng

**Endpoint:** `PUT /api/v1/booking-detail/{booking_detail_id}`

**Mô tả:** Cập nhật số lượng phòng của một item trong giỏ.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "number_of_rooms": 3
}
```

**Response (200 OK):**
```json
{
  "message": "Booking Detail updated successfully",
  "booking_detail": { ... }
}
```

---

## 4. Xóa item khỏi giỏ hàng

**Endpoint:** `DELETE /api/v1/booking-detail/{booking_detail_id}`

**Mô tả:** Xóa một item khỏi giỏ hàng. Chỉ xóa được item trong giỏ chưa thanh toán.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Item đã được xóa khỏi giỏ hàng"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Không thể xóa item từ đơn hàng đã thanh toán"
}
```

---

## Lỗi chung

| Status Code | Mô tả |
|-------------|-------|
| `400 Bad Request` | Tài khoản chưa có thông tin khách hàng |
| `401 Unauthorized` | Token không hợp lệ hoặc hết hạn |
| `404 Not Found` | Không tìm thấy giỏ hàng hoặc item |

---

## Business Rules

1. Mỗi khách hàng chỉ có 1 giỏ hàng active (Booking với status = "pending")
2. Customer ID tự động lấy từ JWT token, không cần FE gửi
3. Chỉ xóa/sửa được item trong giỏ chưa thanh toán
