-- Create extension for UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE salon_db TO salon_user;

-- Optional: Create tables (Flask will create them automatically)
-- But we can create them here for safety
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    created_at VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    service VARCHAR(100) NOT NULL,
    date VARCHAR(20) NOT NULL,
    time VARCHAR(10) NOT NULL,
    booked_at VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active'
);
