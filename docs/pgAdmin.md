# Hướng dẫn kết nối pgAdmin với PostgreSQL Database
## Step 1: Docker compose up
Trong visual Studio mở terminal lên và gõ "docker compose up"

## Step 2: Mở trình duyệt web lên
Truy cập vào http://localhost:8081/browser/
Đăng nhập với tài khoản
username: admin@example.com
password: admin

## Step 3: Regist Server
Ở góc trái Object Explore, mọi người sẽ nhìn thấy hình cái Server
Click chuột phải chọn Register > Server

-- Ở phần General Đặt tên tùy ý VD: localDB
-- Ở phần Connection khai báo như sau
* Host name/address: Các bạn cần điền container ID của container đang chạy PostgreSQL
** Để có ContainerID mọi người mở terminal lên gõ lệnh sau "docker ps"
** Sau đó coppy Cột ContainerID của Container postgres:15
* Port: 5432
* Maintenance database: fastapi_db
* Username: user
* Password: password

Và vậy là đã connect xong

