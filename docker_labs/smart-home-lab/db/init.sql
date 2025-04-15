-- Create the sensors table
CREATE TABLE IF NOT EXISTS sensors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sensor_name VARCHAR(255),
    value FLOAT,
    timestamp DATETIME
);

-- Load data into the sensors table
LOAD DATA INFILE '/var/lib/mysql-files/sensor_data.csv'
INTO TABLE sensors
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(sensor_name, value, timestamp);
