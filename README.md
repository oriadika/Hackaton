
# **Network Speed Test Project**

This project implements a client-server application to measure network performance. It compares **UDP** and **TCP** transfer speeds, supports multiple connections, reports packet loss rates for UDP, and provides detailed performance metrics.

## **Project Overview**

The project is divided into three main components:
1. **Server**: Broadcasts its availability and responds to client requests.
2. **Client**: Listens for server offers, connects to a selected server, and performs speed tests with multiple connections.
3. **Shared Module**: Contains shared constants and utility functions to ensure compatibility between the client and server.

---

## **How to Use**

### **1. Directory Structure**
\`\`\`plaintext
Hackaton/
├── server/
│   └── server.py       # Server implementation
├── client/
│   └── client.py       # Client implementation
├── shared/
│   └── shared.py       # Shared constants and utilities
\`\`\`

### **2. Prerequisites**
- Python 3.x installed on your system.
- Required Python libraries: \`socket\`, \`threading\`, \`struct\`, \`time\`, \`tqdm\`.

### **3. Running the Server**
1. Navigate to the \`server\` directory:
   \`\`\`bash
   cd Hackaton/server
   \`\`\`

2. Start the server:
   \`\`\`bash
   python server.py
   \`\`\`

3. The server will:
   - Broadcast its availability via UDP on port \`13117\`.
   - Listen for TCP and UDP client requests.
   - Handle multiple clients simultaneously using a thread pool.

### **4. Running the Client**
1. Navigate to the \`client\` directory:
   \`\`\`bash
   cd Hackaton/client
   \`\`\`

2. Run the client:
   \`\`\`bash
   python client.py
   \`\`\`

3. Enter the required details:
   - File size (in bytes).
   - Number of TCP connections.
   - Number of UDP connections.

4. Example Workflow:
   - Enter file size: \`1073741824\` (1GB).
   - Enter TCP connections: \`1\`.
   - Enter UDP connections: \`2\`.

5. The client will perform the tests and display real-time progress bars for each connection:
   \`\`\`plaintext
   TCP 1: 100%|██████████| 1.00GB/1.00GB [00:03<00:00, 350MB/s]
   UDP 1: 100%|██████████| 1.00GB/1.00GB [00:02<00:00, 500MB/s]
   UDP 2: 100%|██████████| 1.00GB/1.00GB [00:02<00:00, 520MB/s]
   TCP 1 Complete: Time: 3.50s, Speed: 2800.00 Mbps
   UDP 1 Complete: Time: 2.50s, Speed: 3200.00 Mbps, Success Rate: 98.00%
   UDP 2 Complete: Time: 2.48s, Speed: 3300.00 Mbps, Success Rate: 97.50%
   All transfers complete.
   \`\`\`

---

## **Features**

1. **Support for Multiple Connections**:
   - Handles multiple TCP and UDP connections as specified by the user.
   - Each connection is managed concurrently using threads.

2. **Comprehensive Performance Testing**:
   - Measures transfer speeds for both **TCP** and **UDP**.
   - Reports **packet loss rates** for UDP.

3. **Interactive Client**:
   - Dynamically selects servers based on availability.
   - Prompts users for file size and connection details.
   - Displays real-time progress bars for all active connections.

4. **Multi-Threaded Server**:
   - Uses a thread pool to efficiently handle multiple TCP connections.
   - Handles UDP requests concurrently.

5. **Shared Constants**:
   - Ensures seamless communication between the client and server via the \`shared/shared.py\` module.

6. **Cross-Team Compatibility**:
   - Designed to work with other implementations following the same protocol.

---

## **Testing the Project**

### **Example Scenario**
1. Start the server:
   \`\`\`bash
   python server/server.py
   \`\`\`
   Output:
   \`\`\`plaintext
   Starting server...
   Broadcasting offer...
   Server listening on TCP port 12345
   \`\`\`

2. Start the client:
   \`\`\`bash
   python client/client.py
   \`\`\`

3. Enter the required details:
   \`\`\`plaintext
   Enter file size (bytes): 1073741824
   Enter number of TCP connections: 1
   Enter number of UDP connections: 2
   \`\`\`

4. Observe the results, including progress bars and transfer metrics for all connections.

---

## **Customization**

1. **Change Ports**:
   - Modify \`DEFAULT_UDP_PORT\` and \`DEFAULT_TCP_PORT\` in \`shared/shared.py\` to set custom ports.

2. **Adjust Buffer Size**:
   - Modify \`BUFFER_SIZE\` in \`shared/shared.py\` to optimize for your network.

3. **Timeouts**:
   - Adjust \`UDP_TIMEOUT\` in \`shared/shared.py\` for more or less aggressive timeout handling.

---

## **Troubleshooting**

### **Client Doesn’t Detect Server**
- Ensure the server and client are on the same network.
- Check if UDP broadcasts are allowed in your network.

### **TCP/UDP Transfers Are Slow**
- Test with different buffer sizes (\`BUFFER_SIZE\`) in \`shared/shared.py\`.
- Check for network congestion or interference.

---

## **License**
This project is for educational purposes. Modify and use it freely in the Hackathon.

---
