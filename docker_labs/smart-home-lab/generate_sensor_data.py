import csv
import random
from datetime import datetime, timedelta

# File path for the CSV
output_file = "sensor_data.csv"

# Sensor types
sensor_types = ["Temperature", "Humidity", "Light", "CO2"]

# Generate random data
def generate_sensor_data(records=100):
    data = []
    start_time = datetime.now() - timedelta(hours=records)  # Start time
    for i in range(records):
        sensor_name = random.choice(sensor_types)
        value = round(random.uniform(10, 100), 2)  # Random value between 10 and 100
        timestamp = start_time + timedelta(minutes=i * 10)  # Increment by 10 minutes
        data.append([sensor_name, value, timestamp.strftime("%Y-%m-%d %H:%M:%S")])
    return data

# Write data to CSV
def write_to_csv(data, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["sensor_name", "value", "timestamp"])  # CSV header
        writer.writerows(data)

# Generate and save 100 records
sensor_data = generate_sensor_data(100)
write_to_csv(sensor_data, output_file)

print(f"File '{output_file}' with sensor data generated.")
