# Authentication API Documentation

## Tổng quan

Hệ thống xác thực sử dụng JWT (JSON Web Token) để quản lý phiên đăng nhập. Token được lưu trong database và có thể bị revoke khi đăng xuất.

**Base URL:** `/auth`

---

## 1. Đăng ký tài khoản khách hàng

**Endpoint:** `POST /auth/register`

**Mô tả:** Tạo tài khoản mới cho khách hàng. Tài khoản được kích hoạt ngay lập tức.

**Request Body:**
```json
{
  "username": "customer01",
  "password": "123456"
}
```

**Response (201 Created):**
```json
{
  "message": "Registration successful",
  "account": {
    "account_id": 1,
    "username": "customer01",
    "status": "ACTIVE",
    "created_at": "2025-12-14T10:30:00",
    "roles": ["CUSTOMER"]
  }
}
```

**Lỗi có thể xảy ra:**
- `400 Bad Request` - Username đã tồn tại

---

## 2. Đăng ký tài khoản đối tác

**Endpoint:** `POST /auth/register/partner`

**Mô tả:** Tạo tài khoản đối tác. Tài khoản sẽ ở trạng thái `PENDING` và cần admin duyệt mới được hoạt động.

**Request Body:**
```json
{
  "username": "partner01",
  "password": "123456",
  "name": "Resort ABC",
  "phone_number": "0901234567",
  "address": "123 Đường ABC, Quận 1, TP.HCM",
  "banking_number": "1234567890",
  "bank": "Vietcombank"
}
```

**Response (201 Created):**
```json
{
  "message": "Partner registration submitted. Please wait for admin approval.",
  "partner": {
    "id": 1,
    "account_id": 2,
    "name": "Resort ABC",
    "phone_number": "0901234567",
    "address": "123 Đường ABC, Quận 1, TP.HCM",
    "banking_number": "1234567890",
    "bank": "Vietcombank",
    "account_status": "PENDING"
  }
}
```

---

## 3. Đăng nhập

**Endpoint:** `POST /auth/login`

**Mô tả:** Đăng nhập và nhận JWT token. Chỉ tài khoản có status `ACTIVE` mới đăng nhập được.

**Request Body:**
```json
{
  "username": "customer01",
  "password": "123456"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_at": "2025-12-15T10:30:00"
}
```

**Lỗi có thể xảy ra:**
- `401 Unauthorized` - Sai username/password hoặc tài khoản chưa được kích hoạt

---

## 4. Đăng xuất

**Endpoint:** `POST /auth/logout`

**Mô tả:** Đăng xuất và vô hiệu hóa token hiện tại.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

## 5. Lấy thông tin user hiện tại

**Endpoint:** `GET /auth/me`

**Mô tả:** Lấy thông tin tài khoản đang đăng nhập.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "account_id": 1,
  "username": "customer01",
  "status": "ACTIVE",
  "created_at": "2025-12-14T10:30:00",
  "roles": ["CUSTOMER"]
}
```

---

## Admin APIs

### 6. Xem danh sách đối tác chờ duyệt

**Endpoint:** `GET /api/v1/admin/partners/pending`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "account_id": 2,
    "name": "Resort ABC",
    "phone_number": "0901234567",
    "address": "123 Đường ABC, Quận 1, TP.HCM",
    "banking_number": "1234567890",
    "bank": "Vietcombank",
    "account_status": "PENDING"
  }
]
```

---

### 7. Duyệt/Từ chối đối tác

**Endpoint:** `POST /api/v1/admin/partners/approve`

**Request Body:**
```json
{
  "account_id": 2,
  "approved": true
}
```

| Field | Giá trị | Kết quả |
|-------|---------|---------|
| approved | `true` | Tài khoản chuyển sang `ACTIVE` |
| approved | `false` | Tài khoản chuyển sang `REJECTED` |

**Response (200 OK):**
```json
{
  "message": "Partner registration approved successfully",
  "account_id": 2,
  "status": "ACTIVE"
}
```

---

## Sử dụng Token trong các API khác

Sau khi đăng nhập, thêm header `Authorization` vào mọi request cần xác thực:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Account Status

| Status | Mô tả |
|--------|-------|
| `ACTIVE` | Tài khoản hoạt động bình thường |
| `PENDING` | Đang chờ admin duyệt (chỉ áp dụng cho đối tác) |
| `REJECTED` | Bị từ chối |
| `INACTIVE` | Tài khoản bị vô hiệu hóa |

---

## Cấu hình môi trường

Thêm vào file `.env`:

```env
SECRET_KEY=your-super-secret-key-change-in-production
```
