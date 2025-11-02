-- Reset the public schema (destructive)
-- WARNING: this removes all tables, sequences and data in the public schema.

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- grant to the generic PUBLIC role; specific grants to service accounts are handled by the script
GRANT ALL ON SCHEMA public TO public;
