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
            host='db',           # Service name from docker-compose
            database='smart_home',
            user='root',
            password='rootpassword',
            connect_timeout=10   # Add timeout to prevent hanging
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

            # Create lists for all rows (no deduplication)
            sensor_names = [row['sensor_name'] for row in sensor_data]
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
    print("🚀 Starting Flask Application")
    print("Network and Database Diagnostics Enabled")
    app.run(host='0.0.0.0', port=5000, debug=True)