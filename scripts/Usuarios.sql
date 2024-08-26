-- Create the users table
CREATE TABLE profile (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255),
    role VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    disabled BOOLEAN,
    hashed_password VARCHAR(255) NOT NULL
);
