-- Sample data for development/demo

-- Roles
INSERT INTO role (title) VALUES ('admin') ON CONFLICT DO NOTHING;
INSERT INTO role (title) VALUES ('user') ON CONFLICT DO NOTHING;

-- Accounts
INSERT INTO account (username, password, status) VALUES ('admin', 'adminpass', 'ACTIVE') ON CONFLICT DO NOTHING;
INSERT INTO account (username, password, status) VALUES ('user1', 'user1pass', 'ACTIVE') ON CONFLICT DO NOTHING;

-- Customers
INSERT INTO customer (account_id, fullname, email, phone_number, id_number) VALUES (1, 'Nguyen Van A', 'a@example.com', '0900000001', '123456789') ON CONFLICT DO NOTHING;
INSERT INTO customer (account_id, fullname, email, phone_number, id_number) VALUES (2, 'Tran Thi B', 'b@example.com', '0900000002', '987654321') ON CONFLICT DO NOTHING;

-- Partners
INSERT INTO partner (account_id, name, phone_number, address, banking_number, bank, balance) VALUES (1, 'Vingroup', '0908000001', '123 Main St', '111122223333', 'Vietcombank', 1000000) ON CONFLICT DO NOTHING;
INSERT INTO partner (account_id, name, phone_number, address, banking_number, bank, balance) VALUES (2, 'Du Lich Viet', '0908000002', '456 Side St', '444455556666', 'Techcombank', 2000000) ON CONFLICT DO NOTHING;
-- Citys
INSERT INTO city (name) VALUES ('Hanoi') ON CONFLICT DO NOTHING;
INSERT INTO city (name) VALUES ('Da Nang') ON CONFLICT DO NOTHING;
INSERT INTO city (name) VALUES ('Ho Chi Minh') ON CONFLICT DO NOTHING;
-- Wards
INSERT INTO ward (name, city_id) VALUES ('Ward 1', 1) ON CONFLICT DO NOTHING;
INSERT INTO ward (name, city_id) VALUES ('Ward 2', 2) ON CONFLICT DO NOTHING;
INSERT INTO ward (name, city_id) VALUES ('Ward 3', 3) ON CONFLICT DO NOTHING;
-- Resorts
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (1, 'Resort A', '456 Beach Rd', 1, 'http://img360.com/a.jpg', 5) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (1, 'Resort B', '789 Mountain Rd', 2, 'http://img360.com/b.jpg', 4) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (1, 'Resort C', '123 Lakeview Rd', 3, 'http://img360.com/c.jpg', 3) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (2, 'Resort D', '321 River Rd', 1, 'http://img360.com/d.jpg', 4) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (2, 'Resort E', '654 Forest Rd', 2, 'http://img360.com/e.jpg', 5) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (2, 'Resort F', '987 Desert Rd', 3, 'http://img360.com/f.jpg', 2) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (1, 'Resort A', '456 Beach Rd', 1, 'http://img360.com/a.jpg', 5) ON CONFLICT DO NOTHING;
INSERT INTO resort (partner_id, name, address, ward_id, img_360_url, rating) VALUES (1, 'Resort A', '456 Beach Rd', 1, 'http://img360.com/a.jpg', 5) ON CONFLICT DO NOTHING;
-- Resort Images
INSERT INTO resort_images (resort_id, url) VALUES (1, 'http://images.com/resortA1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (1, 'http://images.com/resortA2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (2, 'http://images.com/resortB1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (2, 'http://images.com/resortB2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (3, 'http://images.com/resortC1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (3, 'http://images.com/resortC2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (4, 'http://images.com/resortD1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (4, 'http://images.com/resortD2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (5, 'http://images.com/resortE1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (5, 'http://images.com/resortE2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (6, 'http://images.com/resortF1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (6, 'http://images.com/resortF2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (7, 'http://images.com/resortA1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (7, 'http://images.com/resortA2.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (8, 'http://images.com/resortA1.jpg') ON CONFLICT DO NOTHING;
INSERT INTO resort_images (resort_id, url) VALUES (8, 'http://images.com/resortA2.jpg') ON CONFLICT DO NOTHING;
-- Room types
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (1, 'Deluxe', 35.0, 'High', 'Luxury', 2, 4, 1500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (1, 'Standard', 25.0, 'Medium', 'Comfort', 1, 2, 1000000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (1, 'Suite', 50.0, 'Premium', 'Elite', 3, 6, 2500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (2, 'Deluxe', 35.0, 'High', 'Luxury', 2, 4, 1500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (2, 'Standard', 25.0, 'Medium', 'Comfort', 1, 2, 1000000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (2, 'Suite', 50.0, 'Premium', 'Elite', 3, 6, 2500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (3, 'Deluxe', 35.0, 'High', 'Luxury', 2, 4, 1500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (3, 'Standard', 25.0, 'Medium', 'Comfort', 1, 2, 1000000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (3, 'Suite', 50.0, 'Premium', 'Elite', 3, 6, 2500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (4, 'Deluxe', 35.0, 'High', 'Luxury', 2, 4, 1500000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (4, 'Standard', 25.0, 'Medium', 'Comfort', 1, 2, 1000000) ON CONFLICT DO NOTHING;
INSERT INTO room_type (resort_id, name, area, quantity_standard, quality_standard, bed_amount, people_amount, price) VALUES (4, 'Suite', 50.0, 'Premium', 'Elite', 3, 6, 2500000) ON CONFLICT DO NOTHING;
-- Rooms
INSERT INTO room (room_type_id, number, status) VALUES (1, 101, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (1, 102, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (2, 201, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (2, 202, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (3, 301, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (3, 302, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (4, 401, 'available') ON CONFLICT DO NOTHING;
INSERT INTO room (room_type_id, number, status) VALUES (4, 402, 'available') ON CONFLICT DO NOTHING;
-- Room Images
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (1, 'http://images.com/roomType1_img1.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (1, 'http://images.com/roomType1_img2.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (1, 'http://images.com/roomType2_img1.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (1, 'http://images.com/roomType2_img2.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (2, 'http://images.com/roomType3_img1.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (2, 'http://images.com/roomType3_img2.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (2, 'http://images.com/roomType4_img1.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (2, 'http://images.com/roomType4_img2.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (3, 'http://images.com/roomType5_img1.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (3, 'http://images.com/roomType5_img2.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (3, 'http://images.com/roomType6_img1.jpg', FALSE) ON CONFLICT DO NOTHING;
INSERT INTO room_images (room_type_id, url, is_deleted) VALUES (3, 'http://images.com/roomType6_img2.jpg', FALSE) ON CONFLICT DO NOTHING;

-- Services
INSERT INTO service (name, resort_id) VALUES ('Spa', 1) ON CONFLICT DO NOTHING;
INSERT INTO service (name, resort_id) VALUES ('Gym', 1) ON CONFLICT DO NOTHING;
INSERT INTO service (name, resort_id) VALUES ('Breakfast', 1) ON CONFLICT DO NOTHING;
INSERT INTO service (name, resort_id) VALUES ('Airport Pickup', 1) ON CONFLICT DO NOTHING;
INSERT INTO service (name, resort_id) VALUES ('Spa', 2) ON CONFLICT DO NOTHING;
INSERT INTO service (name, resort_id) VALUES ('Gym', 2) ON CONFLICT DO NOTHING;
INSERT INTO service (name, resort_id) VALUES ('Breakfast', 2) ON CONFLICT DO NOTHING;
-- Booking
INSERT INTO booking (customer_id, status, cost) VALUES (1, 'confirmed', 2000000) ON CONFLICT DO NOTHING;
INSERT INTO booking (customer_id, status, cost) VALUES (1, 'pending', 2000000) ON CONFLICT DO NOTHING;
-- Offers
INSERT INTO offer (room_type_id, cost) VALUES (1, 2000000) ON CONFLICT DO NOTHING;

-- Booking detail
INSERT INTO booking_detail (booking_id, offer_id, number_of_rooms, cost, started_at, finished_at, status) VALUES (1, 1, 1, 2000000, NOW(), NOW() + INTERVAL '2 days', 'paid') ON CONFLICT DO NOTHING;

-- Invoice
INSERT INTO invoice (customer_id, partner_id, booking_detail_id, cost, finished_time, payment_method) VALUES (1, 1, 1, 2000000, NOW() + INTERVAL '2 days', 'credit_card') ON CONFLICT DO NOTHING;

-- Booking timeslot
INSERT INTO booking_timeslot (room_id, started_time, finished_time, invoice_id) VALUES (1, NOW(), NOW() + INTERVAL '2 days', 1) ON CONFLICT DO NOTHING;

-- Account_asign_role
INSERT INTO account_assign_role (account_id, role_id) VALUES (1, 1) ON CONFLICT DO NOTHING;
INSERT INTO account_assign_role (account_id, role_id) VALUES (2, 2) ON CONFLICT DO NOTHING;
INSERT INTO account_assign_role (account_id, role_id) VALUES (1, 2) ON CONFLICT DO NOTHING;

-- Account_token - Nếu dùng JWT thì không cần lưu token

-- With-draw
INSERT INTO withdraw (partner_id, transaction_amount, status, created_at) VALUES (1, 500000, 'pending', NOW()) ON CONFLICT DO NOTHING;

-- Service-offered
INSERT INTO service_offered (id, offer_id) VALUES (1, 1) ON CONFLICT DO NOTHING;

-- Feedback
INSERT INTO feedback (customer_id, resort_id, rating, comment, created_at) VALUES (1, 1, 5, 'Excellent stay!', NOW()) ON CONFLICT DO NOTHING;
INSERT INTO feedback (customer_id, resort_id, rating, comment, created_at) VALUES (2, 2, 4, 'Very good service.', NOW()) ON CONFLICT DO NOTHING;
INSERT INTO feedback (customer_id, resort_id, rating, comment, created_at) VALUES (1, 2, 3, 'Average experience.', NOW()) ON CONFLICT DO NOTHING;
