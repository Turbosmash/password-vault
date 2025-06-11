-- Create a new database called vaultdb_test 
-- CHARACTER SET utf8mb4 creates the database as UTF-8. This make it possible to use norwegian letters æøå
-- COLLATE utf8mb4_unicode_ci makes data saved in the database "case insensitive". This means that it is possible 
-- to do queries and get results without take into consideraton if the application_name is saved as Steam, STEAM or steam
CREATE DATABASE IF NOT EXISTS password_vault
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Use the newly created database
USE password_vault;

-- Create the User table
-- user_id is given a unique value with AUTO_INCREMENT and is set as a primary key
-- With the use of TIMESTAMP DEFAULT CURRENT_TIMESTAMP, date and time of the created user is automatically added by MySQL
CREATE TABLE IF NOT EXISTS User (
    user_id                 INT AUTO_INCREMENT PRIMARY KEY,
    username                VARCHAR(255) UNIQUE,
    username_password_hash  VARCHAR(255),
    created                 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Vault table
-- item_id is given a unique value with AUTO_INCREMENT and is set as a primary key
-- user_id is set as a foreign key and is referencing user_id in the User table
-- ON DELETE CASCADE ensures that when deleting a user, other connecting rows for that user are deleted in the Vault table
CREATE TABLE IF NOT EXISTS Vault (
    item_id                   INT AUTO_INCREMENT PRIMARY KEY,
    user_id                   INT,
    application_name          VARCHAR(255),
    application_password_cipher VARCHAR(255),
    created                   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated                   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES User(user_id)
        ON DELETE CASCADE
);
