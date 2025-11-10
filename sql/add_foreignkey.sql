
-- ACCOUNT & CUSTOMER
ALTER TABLE customer ADD FOREIGN KEY (account_id) REFERENCES account(account_id);
ALTER TABLE account_token ADD FOREIGN KEY (account_id) REFERENCES account(account_id);
ALTER TABLE account_assign_role ADD FOREIGN KEY (account_id) REFERENCES account(account_id);
ALTER TABLE account_assign_role ADD FOREIGN KEY (role_id) REFERENCES role(id);

-- PARTNER & WITHDRAW
ALTER TABLE partner ADD FOREIGN KEY (account_id) REFERENCES account(account_id);
ALTER TABLE withdraw ADD FOREIGN KEY (partner_id) REFERENCES partner(id);

-- LOCATION
ALTER TABLE ward ADD FOREIGN KEY (city_id) REFERENCES city(id);

-- RESORT & FEEDBACK
ALTER TABLE resort ADD FOREIGN KEY (partner_id) REFERENCES partner(id);
ALTER TABLE resort ADD FOREIGN KEY (ward_id) REFERENCES ward(id);
ALTER TABLE resort_images ADD FOREIGN KEY (resort_id) REFERENCES resort(id);
ALTER TABLE feedback ADD FOREIGN KEY (resort_id) REFERENCES resort(id);
ALTER TABLE feedback ADD FOREIGN KEY (customer_id) REFERENCES customer(id);

-- ROOM & ROOM TYPE
ALTER TABLE room_type ADD FOREIGN KEY (resort_id) REFERENCES resort(id);
ALTER TABLE room_images ADD FOREIGN KEY (room_type_id) REFERENCES room_type(id);
ALTER TABLE room ADD FOREIGN KEY (room_type_id) REFERENCES room_type(id);
ALTER TABLE booking_timeslot ADD FOREIGN KEY (room_id) REFERENCES room(id);

-- SERVICE & OFFER
ALTER TABLE service ADD FOREIGN KEY (resort_id) REFERENCES resort(id);
ALTER TABLE offer ADD FOREIGN KEY (room_type_id) REFERENCES room_type(id);
ALTER TABLE service_offered ADD FOREIGN KEY (offer_id) REFERENCES offer(id);

-- BOOKING & INVOICE
ALTER TABLE booking ADD FOREIGN KEY (customer_id) REFERENCES customer(id);
ALTER TABLE booking_detail ADD FOREIGN KEY (booking_id) REFERENCES booking(id);
ALTER TABLE booking_detail ADD FOREIGN KEY (offer_id) REFERENCES offer(id);
ALTER TABLE invoice ADD FOREIGN KEY (customer_id) REFERENCES customer(id);
ALTER TABLE invoice ADD FOREIGN KEY (partner_id) REFERENCES partner(id);
ALTER TABLE invoice ADD FOREIGN KEY (booking_detail_id) REFERENCES booking_detail(id);