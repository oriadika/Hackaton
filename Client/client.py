import socket
import struct
import time
from tqdm import tqdm
from threading import Thread
import sys
import os
from collections import defaultdict
import curses
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Shared.shared import *


def listen_for_offers():
    """Listen for server offers via UDP."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_socket.bind(('', DEFAULT_UDP_PORT))

    print(f"{bcolors.OKCYAN}Listening for server offers...{bcolors.ENDC}")
    while True:
        try:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            magic_cookie, message_type, udp_port, tcp_port = struct.unpack(OFFER_FORMAT, data)
            if magic_cookie == MAGIC_COOKIE and message_type == MESSAGE_TYPE_OFFER:
                print(f"{bcolors.OKGREEN}Offer received from {addr[0]}: UDP Port {udp_port}, TCP Port {tcp_port}{bcolors.ENDC}")
                return addr[0], udp_port, tcp_port
        except Exception as e:
            print(f"{bcolors.FAIL}Error listening for offers: {e}{bcolors.ENDC}")

def perform_tcp_connection(server_ip, tcp_port, file_size, connection_id, stats):
    """Perform a TCP file transfer."""
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
                stats['total_bytes'] += len(data)
            progress.close()

        elapsed_time = time.time() - start_time
        stats['elapsed_time'] += elapsed_time
        speed = (file_size * 8) / elapsed_time
        print(f"{bcolors.OKGREEN}TCP {connection_id} Complete: Time: {elapsed_time:.2f}s, Speed: {speed:.2f} bits/s{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}Error during TCP {connection_id}: {e}{bcolors.ENDC}")

def perform_udp_connection(server_ip, udp_port, file_size, connection_id, stats):
    """Perform a UDP file transfer."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(UDP_TIMEOUT)

    request_packet = struct.pack(REQUEST_FORMAT, MAGIC_COOKIE, MESSAGE_TYPE_REQUEST, file_size)
    udp_socket.sendto(request_packet, (server_ip, udp_port))

    received_segments = 0
    total_segments = (file_size + BUFFER_SIZE - 1) // BUFFER_SIZE
    missing_segments = set(range(total_segments))
    start_time = time.time()

    progress = tqdm(total=file_size, unit='B', unit_scale=True, desc=f"UDP {connection_id}")
    while True:
        try:
            data, _ = udp_socket.recvfrom(BUFFER_SIZE + 20)
            magic_cookie, message_type, total_segments, segment_number = struct.unpack(PAYLOAD_FORMAT, data[:21])
            if magic_cookie == MAGIC_COOKIE and message_type == MESSAGE_TYPE_PAYLOAD:
                if segment_number in missing_segments:
                    received_segments += 1
                    missing_segments.remove(segment_number)
                progress.update(BUFFER_SIZE)
                stats['total_bytes'] += BUFFER_SIZE
        except socket.timeout:
            break

    progress.close()

    elapsed_time = time.time() - start_time
    stats['elapsed_time'] += elapsed_time
    success_rate = (received_segments / total_segments) * 100 if total_segments else 0
    speed = (received_segments * BUFFER_SIZE * 8) / elapsed_time
    print(f"{bcolors.OKBLUE}UDP {connection_id} Complete: Time: {elapsed_time:.2f}s, Speed: {speed:.2f} bits/s, Success Rate: {success_rate:.2f}%{bcolors.ENDC}")

def monitor_stats(stats, active_transfers):
    """Continuously display real-time stats."""
    while active_transfers.is_set():
        speed = (stats['total_bytes'] * 8) / max(1, stats['elapsed_time'])
        print(f"{bcolors.OKGREEN}Real-Time Stats: Speed: {speed:.2f} bits/s, Bytes Transferred: {stats['total_bytes']}{bcolors.ENDC}", end="\r")
        time.sleep(1)

def main():
    server_ip, udp_port, tcp_port = listen_for_offers()

    # Prompt user for details
    file_size = int(input(f"{bcolors.HEADER}Enter file size (bytes): {bcolors.ENDC}"))
    tcp_connections = int(input(f"{bcolors.HEADER}Enter number of TCP connections: {bcolors.ENDC}"))
    udp_connections = int(input(f"{bcolors.HEADER}Enter number of UDP connections: {bcolors.ENDC}"))

    # Shared stats for monitoring
    stats = {'total_bytes': 0, 'elapsed_time': 0}
    active_transfers = threading.Event()
    active_transfers.set()

    # Start real-time monitoring
    monitor_thread = threading.Thread(target=monitor_stats, args=(stats, active_transfers))
    monitor_thread.start()

    # Perform TCP and UDP connections
    threads = []

    # Start TCP connections
    for i in range(tcp_connections):
        thread = Thread(target=perform_tcp_connection, args=(server_ip, tcp_port, file_size, i + 1, stats))
        thread.start()
        threads.append(thread)

    # Start UDP connections
    for i in range(udp_connections):
        thread = Thread(target=perform_udp_connection, args=(server_ip, udp_port, file_size, i + 1, stats))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Stop monitoring
    active_transfers.clear()
    monitor_thread.join()

    print(f"{bcolors.OKGREEN}All transfers complete.{bcolors.ENDC}")

    print(f"{bcolors.OKGREEN}All transfers complete.{bcolors.ENDC}")

if __name__ == "__main__":
    main()
