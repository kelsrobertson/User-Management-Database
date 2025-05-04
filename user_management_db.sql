# One-to-many relationship
CREATE DATABASE user_management_db;
USE user_management_db;

CREATE TABLE userauthentication (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE sessions (
    session_id VARCHAR(255) PRIMARY KEY, 
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES userauthentication(user_id)
);

CREATE TABLE useractions (
    action_id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT NOT NULL,
    action_description VARCHAR(255) NOT NULL,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES userauthentication(user_id)
);
