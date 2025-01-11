# shared/shared.py
#Constants and shared functions for the Hackathon project

# Magic Cookie and Message Types
MAGIC_COOKIE = 0xabcddcba
MESSAGE_TYPE_OFFER = 0x2
MESSAGE_TYPE_REQUEST = 0x3
MESSAGE_TYPE_PAYLOAD = 0x4

# Default Ports
DEFAULT_UDP_PORT = 13117
DEFAULT_TCP_PORT = 12345

# Buffer Size
BUFFER_SIZE = 1024

# Packet Formats
OFFER_FORMAT = "!IBHH"  # Magic cookie, message type, UDP port, TCP port
REQUEST_FORMAT = "!IBQ"  # Magic cookie, message type, file size
PAYLOAD_FORMAT = "!IBQQ"  # Magic cookie, message type, total segments, current segment

# Timeouts
UDP_TIMEOUT = 1  # 1 second timeout for UDP transfers
