# Server Implementation with ThreadPool

import socket
from concurrent.futures import ThreadPoolExecutor
import struct
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../Shared'))
from Shared.shared import *


def broadcast_offers():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    offer_packet = struct.pack(OFFER_FORMAT, MAGIC_COOKIE, MESSAGE_TYPE_OFFER, DEFAULT_UDP_PORT, DEFAULT_TCP_PORT)

    while True:
        udp_socket.sendto(offer_packet, ('<broadcast>', DEFAULT_UDP_PORT))
        print("Broadcasting offer...")
        time.sleep(1)

def handle_tcp_connection(conn, addr):
    try:
        data = conn.recv(BUFFER_SIZE).decode('utf-8').strip()
        requested_size = int(data)
        print(f"TCP Request from {addr}: {requested_size} bytes")

        total_sent = 0
        while total_sent < requested_size:
            chunk_size = min(BUFFER_SIZE, requested_size - total_sent)
            conn.send(b'X' * chunk_size)
            total_sent += chunk_size

        print(f"Sent {total_sent} bytes to {addr} via TCP")
    except Exception as e:
        print(f"Error in TCP connection: {e}")
    finally:
        conn.close()

def handle_udp_request(udp_socket, client_addr, requested_size):
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

def handle_udp_connections():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', DEFAULT_UDP_PORT))

    while True:
        try:
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)
            magic_cookie, message_type, file_size = struct.unpack(REQUEST_FORMAT, data)
            if magic_cookie == MAGIC_COOKIE and message_type == MESSAGE_TYPE_REQUEST:
                print(f"Valid UDP request from {addr}: {file_size} bytes")
                handle_udp_request(udp_socket, addr, file_size)
        except Exception as e:
            print(f"Error handling UDP request: {e}")

def start_server():
    thread_pool = ThreadPoolExecutor(max_workers=10)

    threading.Thread(target=broadcast_offers, daemon=True).start()

    threading.Thread(target=handle_udp_connections, daemon=True).start()

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', DEFAULT_TCP_PORT))
    tcp_socket.listen()

    print(f"Server listening on TCP port {DEFAULT_TCP_PORT}")
    while True:
        conn, addr = tcp_socket.accept()
        thread_pool.submit(handle_tcp_connection, conn, addr)

if __name__ == "__main__":
    print("Starting server...")
    start_server()