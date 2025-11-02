# Hướng dẫn reset dữ liệu

## Reset Table
Get-Content .\sql\reset_schema.sql | docker exec -i is207-be-db-1 psql -U user -d fastapi_db -v ON_ERROR_STOP=1

## Khởi tạo Table theo file init.sql
Get-Content .\sql\init.sql | docker exec -i is207-be-db-1 psql -U user -d fastapi_db -v ON_ERROR_STOP=1

## Thêm dữ liệu mẫu (insert sample data)
Get-Content .\sql\insert_data.sql | docker exec -i is207-be-db-1 psql -U user -d fastapi_db -v ON_ERROR_STOP=1