FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=smart_home

# Copy the sensor data CSV file
COPY sensor_data.csv /var/lib/mysql-files/sensor_data.csv

# Copy initialization SQL script
COPY init.sql /docker-entrypoint-initdb.d/
