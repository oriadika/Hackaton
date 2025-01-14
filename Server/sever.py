# Server Implementation with ThreadPool

import socket
from concurrent.futures import ThreadPoolExecutor
import threading
import struct
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Shared.shared import *



def broadcast_offers():
    """Broadcast UDP offers to clients."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    offer_packet = struct.pack(OFFER_FORMAT, MAGIC_COOKIE, MESSAGE_TYPE_OFFER, DEFAULT_UDP_PORT, DEFAULT_TCP_PORT)

    while True:
        udp_socket.sendto(offer_packet, ('<broadcast>', DEFAULT_UDP_PORT))
        print(f"{bcolors.OKCYAN}Broadcasting offer...{bcolors.ENDC}")
        time.sleep(1)

def handle_tcp_connection(conn, addr):
    """Handle incoming TCP requests."""
    try:
        data = conn.recv(BUFFER_SIZE).decode('utf-8').strip()
        requested_size = int(data)
        print(f"{bcolors.OKBLUE}TCP Request from {addr}: {requested_size} bytes{bcolors.ENDC}")

        total_sent = 0
        while total_sent < requested_size:
            chunk_size = min(BUFFER_SIZE, requested_size - total_sent)
            conn.send(b'X' * chunk_size)
            total_sent += chunk_size

        print(f"{bcolors.OKGREEN}Sent {total_sent} bytes to {addr} via TCP{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}Error in TCP connection: {e}{bcolors.ENDC}")
    finally:
        conn.close()

def handle_udp_request(udp_socket, client_addr, requested_size):
    """Handle incoming UDP requests."""
    total_segments = (requested_size + BUFFER_SIZE - 1) // BUFFER_SIZE
    for segment_number in range(total_segments):
        payload_packet = struct.pack(
            PAYLOAD_FORMAT,
            MAGIC_COOKIE,
            MESSAGE_TYPE_PAYLOAD,
            total_segments,
            segment_number
        ) + b'X' * BUFFER_SIZE
        udp_socket.sendto(payload_packet, client_addr)
        print(f"{bcolors.OKCYAN}Sent segment {segment_number + 1}/{total_segments} to {client_addr}{bcolors.ENDC}")

def handle_udp_connections():
    """Listen for UDP requests and respond to clients."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    udp_socket.bind(('', DEFAULT_UDP_PORT))
    
    while True:
        try:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            magic_cookie, message_type, file_size = struct.unpack(REQUEST_FORMAT, data)
            if magic_cookie == MAGIC_COOKIE and message_type == MESSAGE_TYPE_REQUEST:
                print(f"{bcolors.OKCYAN}Valid UDP request from {addr}: {file_size} bytes{bcolors.ENDC}")
                handle_udp_request(udp_socket, addr, file_size)
            else:
                print(f"{bcolors.WARNING}Invalid UDP packet from {addr}{bcolors.ENDC}")
        except Exception as e:
            print(f"{bcolors.FAIL}Error handling UDP request: {e}{bcolors.ENDC}")

def start_server():
    """Start the server."""
    thread_pool = ThreadPoolExecutor(max_workers=10)

    threading.Thread(target=broadcast_offers, daemon=True).start()
    threading.Thread(target=handle_udp_connections, daemon=True).start()

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', DEFAULT_TCP_PORT))
    tcp_socket.listen()

    print(f"{bcolors.HEADER}Server listening on TCP port {DEFAULT_TCP_PORT}{bcolors.ENDC}")
    while True:
        conn, addr = tcp_socket.accept()
        thread_pool.submit(handle_tcp_connection, conn, addr)

if __name__ == "__main__":
    print(f"{bcolors.OKGREEN}Starting server...{bcolors.ENDC}")
    start_server()
