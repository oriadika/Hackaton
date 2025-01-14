# Constants and shared functions for the Hackathon project

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
REQUEST_FORMAT = "!IBQ"  # Magic Cookie (4 bytes), Message Type (1 byte), File Size (8 bytes)
PAYLOAD_FORMAT = "!IBQQ"  # Magic cookie, message type, total segments, current segment

# Timeouts
UDP_TIMEOUT = 1  # 1 second timeout for UDP transfers
