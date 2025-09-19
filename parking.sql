
CREATE DATABASE parking_db;

USE parking_db;

CREATE TABLE parking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    vehicle_type VARCHAR(20),
    entry_time DATETIME,
    exit_time DATETIME,
    parking_fee FLOAT
);

select * from parking;