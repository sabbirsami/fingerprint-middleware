
import socket
import configparser

def connect_to_device(ip, port):
    """Connect to the fingerprint device."""
    try:
        device_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        device_socket.connect((ip, port))
        print("Connected to the fingerprint device.")
        return device_socket
    except Exception as e:
        print(f"Error connecting to the device: {e}")
        return None

def receive_attendance_data(device_socket):
    """Receive attendance data from the fingerprint device."""
    try:
        while True:
            data = device_socket.recv(1024)  # Adjust buffer size as needed
            if not data:
                break
            # Process the attendance data here
            print(f"Received attendance data: {data.decode()}")
    except Exception as e:
        print(f"Error receiving attendance data: {e}")

def load_config():
    """Load configuration from config.ini file."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['FingerprintDevice']

def main():
    fingerprint_device_config = load_config()

    fingerprint_device_ip = fingerprint_device_config['IP']
    fingerprint_device_port = int(fingerprint_device_config['Port'])

    device_socket = connect_to_device(fingerprint_device_ip, fingerprint_device_port)
    if device_socket:
        receive_attendance_data(device_socket)
        device_socket.close()

if __name__ == "__main__":
    main()
