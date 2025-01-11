import socket
import struct
import time
from tqdm import tqdm
from threading import Thread
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../Shared'))
from Shared.shared import *


def listen_for_offers():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_socket.bind(('', DEFAULT_UDP_PORT))

    print("Listening for server offers...")
    while True:
        try:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            magic_cookie, message_type, udp_port, tcp_port = struct.unpack(OFFER_FORMAT, data)
            if magic_cookie == MAGIC_COOKIE and message_type == MESSAGE_TYPE_OFFER:
                print(f"Offer received from {addr[0]}: UDP Port {udp_port}, TCP Port {tcp_port}")
                return addr[0], udp_port, tcp_port
        except Exception as e:
            print(f"Error listening for offers: {e}")

def perform_tcp_connection(server_ip, tcp_port, file_size, connection_id):
    try:
        start_time = time.time()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((server_ip, tcp_port))
            tcp_socket.sendall(f"{file_size}\n".encode('utf-8'))

            received = 0
            progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=f"TCP {connection_id}")
            while received < file_size:
                data = tcp_socket.recv(BUFFER_SIZE)
                received += len(data)
                progress.update(len(data))
            progress.close()

        elapsed_time = time.time() - start_time
        speed = (file_size * 8) / elapsed_time
        print(f"TCP {connection_id} Complete: Time: {elapsed_time:.2f}s, Speed: {speed:.2f} bits/s")
    except Exception as e:
        print(f"Error during TCP {connection_id}: {e}")

def perform_udp_connection(server_ip, udp_port, file_size, connection_id):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(UDP_TIMEOUT)

    request_packet = struct.pack(REQUEST_FORMAT, MAGIC_COOKIE, MESSAGE_TYPE_REQUEST, file_size)
    udp_socket.sendto(request_packet, (server_ip, udp_port))

    received_segments = 0
    total_segments = None
    start_time = time.time()

    progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=f"UDP {connection_id}")
    while True:
        try:
            data, _ = udp_socket.recvfrom(BUFFER_SIZE + 20)
            magic_cookie, message_type, total_segments, segment_number = struct.unpack(PAYLOAD_FORMAT, data[:21])
            if magic_cookie == MAGIC_COOKIE and message_type == MESSAGE_TYPE_PAYLOAD:
                received_segments += 1
                progress.update(BUFFER_SIZE)
        except socket.timeout:
            break

    progress.close()

    elapsed_time = time.time() - start_time
    success_rate = (received_segments / total_segments) * 100 if total_segments else 0
    speed = (received_segments * BUFFER_SIZE * 8) / elapsed_time
    print(f"UDP {connection_id} Complete: Time: {elapsed_time:.2f}s, Speed: {speed:.2f} bits/s, Success Rate: {success_rate:.2f}%")

def main():
    server_ip, udp_port, tcp_port = listen_for_offers()
    
    # Prompt user for details
    file_size = int(input("Enter file size (bytes): "))
    tcp_connections = int(input("Enter number of TCP connections: "))
    udp_connections = int(input("Enter number of UDP connections: "))

    # Perform TCP and UDP connections
    threads = []

    # Start TCP connections
    for i in range(tcp_connections):
        thread = Thread(target=perform_tcp_connection, args=(server_ip, tcp_port, file_size, i + 1))
        thread.start()
        threads.append(thread)

    # Start UDP connections
    for i in range(udp_connections):
        thread = Thread(target=perform_udp_connection, args=(server_ip, udp_port, file_size, i + 1))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All transfers complete.")

if __name__ == "__main__":
    main()
