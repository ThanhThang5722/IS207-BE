-- ===============================
-- ACCOUNT & CUSTOMER
-- ===============================

CREATE TABLE IF NOT EXISTS account (
  account_id SERIAL PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  status VARCHAR(20) DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS customer (
  id SERIAL PRIMARY KEY,
  account_id INT,
  fullname VARCHAR(100),
  email VARCHAR(150) UNIQUE,
  phone_number VARCHAR(10),
  id_number VARCHAR(15),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS role (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS account_token (
  token_id SERIAL PRIMARY KEY,
  account_id INT,
  token_value VARCHAR(500) NOT NULL,
  expires_at TIMESTAMP,
  issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_revoked BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS account_assign_role (
  account_id INT,
  role_id INT,
  PRIMARY KEY (account_id, role_id)
);

-- ===============================
-- PARTNER & WITHDRAW
-- ===============================

CREATE TABLE IF NOT EXISTS partner (
  id SERIAL PRIMARY KEY,
  account_id INT,
  name VARCHAR(100),
  phone_number VARCHAR(10),
  address VARCHAR(255),
  banking_number VARCHAR(20),
  bank VARCHAR(255),
  balance NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS withdraw (
  id SERIAL PRIMARY KEY,
  partner_id INT,
  transaction_amount NUMERIC(12,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  finished_at TIMESTAMP,
  status VARCHAR(255)
);

-- ===============================
-- LOCATION TABLES
-- ===============================

CREATE TABLE IF NOT EXISTS city (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ward (
  id SERIAL PRIMARY KEY,
  city_id INT,
  name VARCHAR(255)
);

-- ===============================
-- RESORT & FEEDBACK
-- ===============================

CREATE TABLE IF NOT EXISTS resort (
  id SERIAL PRIMARY KEY,
  partner_id INT,
  name VARCHAR(255),
  address VARCHAR(255),
  ward_id INT,
  img_360_url VARCHAR(255),
  rating INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS resort_images (
  id SERIAL PRIMARY KEY,
  resort_id INT,
  url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS feedback (
  id SERIAL PRIMARY KEY,
  resort_id INT,
  customer_id INT,
  rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================
-- ROOM & ROOM TYPE
-- ===============================

CREATE TABLE IF NOT EXISTS room_type (
  id SERIAL PRIMARY KEY,
  resort_id INT,
  name VARCHAR(255),
  area FLOAT,
  quantity_standard VARCHAR(255),
  quality_standard VARCHAR(255),
  bed_amount INT,
  people_amount INT,
  price NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS room_images (
  id SERIAL PRIMARY KEY,
  room_type_id INT,
  url VARCHAR(255),
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS room (
  id SERIAL PRIMARY KEY,
  room_type_id INT,
  number INT,
  status VARCHAR(255),
  UNIQUE (room_type_id, number)
);

CREATE TABLE IF NOT EXISTS booking_timeslot (
  room_id INT,
  started_time TIMESTAMP,
  finished_time TIMESTAMP,
  invoice_id INT,
  PRIMARY KEY (room_id, started_time)
);

-- ===============================
-- SERVICE & OFFER
-- ===============================

CREATE TABLE IF NOT EXISTS service (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  resort_id INT
);

CREATE TABLE IF NOT EXISTS offer (
  id SERIAL PRIMARY KEY,
  room_type_id INT,
  cost NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS service_offered (
  id SERIAL PRIMARY KEY,
  offer_id INT
);

-- ===============================
-- BOOKING & INVOICE
-- ===============================

CREATE TABLE IF NOT EXISTS booking (
  id SERIAL PRIMARY KEY,
  customer_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(255),
  cost NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS booking_detail (
  id SERIAL PRIMARY KEY,
  booking_id INT,
  offer_id INT,
  number_of_rooms INT,
  cost NUMERIC(12,2),
  started_at TIMESTAMP,
  finished_at TIMESTAMP,
  status VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS invoice (
  id SERIAL PRIMARY KEY,
  customer_id INT,
  partner_id INT,
  booking_detail_id INT,
  cost NUMERIC(12,2),
  finished_time TIMESTAMP,
  payment_method VARCHAR(255)
);