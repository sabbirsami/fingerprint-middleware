import socket
import configparser
import logging
import time

def connect_to_device(ip, port):
    """Connect to the fingerprint device."""
    try:
        device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        device_socket.settimeout(10)  # Set a timeout of 10 seconds for connection
        device_socket.connect((ip, port))
        print("ip port, ", ip, port)
        logging.info("Connected to the fingerprint device.")
        return device_socket
    except socket.error as e:
        logging.error(f"Error connecting to the device: {e}")
        return None

def receive_attendance_data(device_socket):
    """Receive attendance data from the fingerprint device."""
    try:
        while True:
            data = device_socket.recv(1024)  # Adjust buffer size as needed
            
            if not data:
                logging.info("Connection closed by the device.")
                break
            logging.info(f"Received attendance data (hex): {data.hex()}")
            logging.info(f"Received attendance data (decoded): {data.decode()}")
            print(data.decode())
    except socket.error as e:
        logging.error(f"Error receiving attendance data: {e}")

def load_config():
    """Load configuration from config.ini file."""
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        return config['FingerprintDevice']
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return None

def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        filename='middleware.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    setup_logging()

    while True:
        fingerprint_device_config = load_config()

        if fingerprint_device_config is None:
            logging.error("Configuration not loaded. Exiting.")
            break

        fingerprint_device_ip = fingerprint_device_config.get('IP')
        fingerprint_device_port = int(fingerprint_device_config.get('Port'))

        if not fingerprint_device_ip or not fingerprint_device_port:
            logging.error("IP address or port not specified in configuration. Exiting.")
            break

        device_socket = connect_to_device(fingerprint_device_ip, fingerprint_device_port)
        if device_socket:
            receive_attendance_data(device_socket)
            device_socket.close()

        # Wait for a while before attempting to reconnect
        time.sleep(10)

if __name__ == "__main__":
    main()
