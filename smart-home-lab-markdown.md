# Chapter 9 Lab03: Deploying a Multi-Container Application Using Docker Compose

## Objective
In this lab, you will deploy a simple smart home application that consists of:
- A Flask application (app), which will serve as the backend.
- A MySQL database (db), storing the smart home data.
- An Nginx server (nginx), acting as a reverse proxy for the Flask application.

By the end of this lab, you will have learned how to use Docker Compose to manage multi-container applications and configure services to work together in a networked environment.

## Prerequisites
- Basic understanding of Docker and Docker Compose.
- Docker and Docker Compose installed on your local machine.

## Lab Steps

### Step 1: Set Up the Project Directory

**Project structure:**

1. Create a project directory called `smart_home`:
```bash
$ mkdir smart_home
$ cd smart_home
```

2. Inside the smart_home directory, create the following folder structure:
```bash
$ mkdir app db nginx
```

3. Copy the necessary files into each folder:
   - The docker-compose.yaml file should be placed in the smart_home directory.
   - Place Dockerfile, requirements.txt, and the application code inside the app folder.
   - Place the default.conf file in the nginx folder.
   - Add init.sql to the db folder if needed for initial database setup.

### Step 2: Build the Application Docker Image

1. In the app folder, create the following files:

**Dockerfile:**
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9
# Set the working directory
WORKDIR /app
# Copy application files
COPY . .
# Install dependencies
RUN pip install -r requirements.txt
# Expose Flask port
EXPOSE 5000
# Run the application
CMD ["python", "app.py"]
```

**Requirements.txt:**
```
flask
mysql-connector-python
```

2. Add a basic Flask application (app.py) to the app folder:

**app.py:**
```python
import os
import socket
import traceback
from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    """Establish MySQL database connection with detailed logging"""
    try:
        connection = mysql.connector.connect(
            host='db', # Service name from docker-compose
            database='smart_home',
            user='root',
            password='rootpassword',
            connect_timeout=10 # Add timeout to prevent hanging
        )
        return connection
    except Error as e:
        print(f"MySQL Connection Error: {e}")
        return None

@app.route('/')
def dashboard():
    """Main dashboard route with sensor data retrieval"""
    connection = None
    try:
        connection = get_db_connection()
        if connection and connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Fetch sensor data
            cursor.execute("""
                SELECT sensor_name, value, timestamp
                FROM sensors
                ORDER BY timestamp DESC
            """)
            sensor_data = cursor.fetchall()
            
            # Preserve order and get unique sensor names
            sensor_names = []
            seen_sensors = set()
            for row in sensor_data:
                if row['sensor_name'] not in seen_sensors:
                    sensor_names.append(row['sensor_name'])
                    seen_sensors.add(row['sensor_name'])
            
            values = [row['value'] for row in sensor_data]
            timestamps = [str(row['timestamp']) for row in sensor_data]
            cursor.close()
            
            # Render dashboard with sensor data
            return render_template('dashboard.html',
                                  sensor_names=sensor_names,
                                  values=values,
                                  timestamps=timestamps)
        else:
            # If database connection fails, render with error
            return render_template('dashboard.html',
                                  sensor_names=[],
                                  values=[],
                                  timestamps=[]), 500
    except Exception as e:
        print("Error in dashboard:")
        print(traceback.format_exc())
        # Render with empty data in case of error
        return render_template('dashboard.html',
                              sensor_names=[],
                              values=[],
                              timestamps=[]), 500
    finally:
        # Ensure connection is closed
        if connection and connection.is_connected():
            connection.close()

@app.route('/network-test')
def network_test():
    """Endpoint for network diagnostics"""
    try:
        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        try:
            db_ip = socket.gethostbyname('db')
            connection_test = get_db_connection()
            db_status = "Connected" if connection_test else "Connection Failed"
            if connection_test:
                connection_test.close()
        except Exception as db_error:
            db_status = f"Error: {db_error}"
        
        return f"""
        Network Diagnostics:
        - Hostname: {hostname}
        - Host IP: {host_ip}
        - DB Hostname Resolution: db -> {db_ip}
        - Database Connection: {db_status}
        """
    except Exception as e:
        return f"Network Test Error: {e}", 500

if __name__ == '__main__':
    print("")
    print("Network and Database Diagnostics Enabled")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

3. Inside the app/templates directory, create a basic dashboard.html to display data:

**templates/dashboard.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Home Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #007BFF;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .container {
            width: 80%;
            margin: 20px auto;
        }
    </style>
</head>
<body>
    <header>
        <h1>Smart Home Sensors Dashboard</h1>
    </header>
    <div class="container">
        <canvas id="sensorChart"></canvas>
    </div>
    <script>
        // Pass Python data into JavaScript
        const sensorNames = {{ sensor_names|tojson }};
        const values = {{ values|tojson }};
        const timestamps = {{ timestamps|tojson }};
        
        // Create data points with explicit labels
        const dataPoints = values.map((value, index) => ({
            x: timestamps[index],
            y: value,
            sensorName: sensorNames[index]
        }));
        
        // Set up the chart
        const ctx = document.getElementById('sensorChart').getContext('2d');
        const sensorChart = new Chart(ctx, {
            type: 'line', // Line chart
            data: {
                labels: timestamps, // X-axis labels (timestamps)
                datasets: [{
                    label: 'Sensor Values',
                    data: dataPoints,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 2,
                    tension: 0.4 // Smooth curve
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const dataPoint = context.dataset.data[context.dataIndex];
                                return `${dataPoint.sensorName}: ${dataPoint.y}`;
                            }
                        }
                    },
                    datalabels: {
                        display: true,
                        color: 'black',
                        anchor: 'end',
                        align: 'top',
                        formatter: function(value, context) {
                            return context.dataset.data[context.dataIndex].sensorName;
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Timestamp'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Sensor Value'
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
```

### Step 3: Configure the Nginx Reverse Proxy

In the `nginx` folder, create the `default.conf` file to configure Nginx to proxy requests to the Flask application:

**nginx/default.conf:**
```nginx
server {
    listen 80;
    server_name localhost;
    
    location / {
        proxy_pass http://app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 4: Database Container Configuration (db)

1. Create a `Dockerfile` (db/Dockerfile):
```dockerfile
FROM mysql:8.0
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=smart_home
# Copy initialization SQL script
COPY init.sql /docker-entrypoint-initdb.d/
# Copy the sensor data CSV file
COPY sensor_data.csv /var/lib/mysql-files/sensor_data.csv
```

2. Create the SQL Initialization Script (`db/init.sql`)
This script creates a sensor_data table and populates it with data from sensor_data.csv (this file will be given to students):
```sql
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
```

Here is an example of the data in the sensor_data.csv file:
```
SENSOR_NAME,VALUE,TIMESTAMP
Temperature,85.42,2024-12-07 16:58:52
Humidity,31.49,2024-12-07 17:38:52
CO2,18.89,2024-12-07 17:28:52
```

### Step 5: Creating Docker Compose File

In the root of the project (smart_home), create a docker-compose.yaml file:

**docker-compose.yaml:**
```yaml
services:
  db:
    image: mysql:8.0
    container_name: mysql_db
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: smart_home
      MYSQL_USER: root
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
  
  app:
    build:
      context: ./app
    container_name: flask_app
    environment:
      FLASK_APP: app.py
      FLASK_ENV: development
    ports:
      - "5000:5000"
    depends_on:
      - db
  
  nginx:
    image: nginx:alpine
    container_name: nginx_server
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app

volumes:
  mysql_data:

networks:
  smart_home_network:
    driver: bridge
```

### Step 6: Build and Run the Application

1. From the root directory (`smart_home`), run the following command to build and start all the services:
```bash
$ docker-compose up --build
```

2. Once the services are up and running, open your browser and navigate to http://localhost:5000. You should see the Smart Home Dashboard displaying devices and their statuses.

### Step 7: Modify the Application

Note that you can make changes to your app source file and just run the docker compose command again.

1. Modify the app.py file or the dashboard.html template to change the application's behavior or display additional data.
2. After modifying the code, rebuild the app container:
```bash
$ docker-compose up --build app
```

### Step 8: Exploration and Container Management Tasks

While the containers are running, perform the following tasks to explore and manage the containers:

1. Inspect Container Information
   - Use `docker ps` to list all running containers and their details.
   - Run `docker inspect <container_name>` to get detailed information about a specific container, such as:
     - IP address
     - Mounted volumes
     - Environment variables

Example:
```bash
$ docker inspect mysql_db | grep IPAddress
$ docker inspect flask_app | grep IPAddress
$ docker inspect nginx_server | grep IPAddress
```

### Step 9: Access the Shell of a Running Container

- Use `docker exec -it <container_name> /bin/bash` to access the shell of a container.
- Once inside, check network configurations:
```bash
$ ifconfig
$ ping flask_app
$ ping mysql_db
```

### Step 10: Check Logs

Use `docker logs <container_name>` to view logs for a specific container. For example:
```bash
$ docker logs flask_app
$ docker logs mysql_db
$ docker logs nginx_server
```

### Step 11: Explore Networks

- List all Docker networks:
```bash
$ docker network ls
```

- Inspect the custom network created by Docker Compose (`smart_home_network`):
```bash
$ docker network inspect smart_home_network
```

### Step 12: Concluding the lab

Once you are done with the lab, use the following command to shutdown all the containers:
```bash
$ docker-compose down
```
