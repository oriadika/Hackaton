
# **Network Speed Test - Client & Server**

## **Project Overview**
This project implements a client-server application to test network speed using both **TCP** and **UDP** protocols. The client measures download speeds and success rates when transferring data from the server. The system is designed to handle concurrent connections and supports real-time performance monitoring.

---

## **Features**
- **UDP and TCP File Transfers**:
  - Measure speed and performance over reliable (TCP) and unreliable (UDP) protocols.
- **Real-Time Monitoring**:
  - Displays live updates of transfer speed and bytes transferred during the download.
- **Multithreading**:
  - Supports multiple simultaneous TCP and UDP connections.
- **Advanced Metrics**:
  - Calculates jitter, latency, and packet success rates for UDP transfers.
- **Color-Coded Logs**:
  - Provides visually distinct logs using ANSI colors for better readability.

---

## **Setup**

### **Prerequisites**
- Python 3.8 or higher.
- Install required libraries:
  ```bash
  pip install tqdm
  ```

### **Directory Structure**
```
.
├── client.py          # Client-side application
├── server.py          # Server-side application
├── Shared/
│   ├── shared.py      # Shared constants and formats
└── README.md          # Documentation
```

---

## **How to Run**

### **Step 1: Start the Server**
1. Open a terminal and navigate to the project directory.
2. Run the server:
   ```bash
   python server.py
   ```
3. The server will:
   - Broadcast its availability via UDP.
   - Listen for TCP and UDP file transfer requests.

### **Step 2: Start the Client**
1. Open another terminal and navigate to the project directory.
2. Run the client:
   ```bash
   python client.py
   ```
3. Follow the prompts:
   - Enter the file size (in bytes) to download.
   - Specify the number of TCP and UDP connections.

4. The client will:
   - Detect the server via UDP broadcasts.
   - Perform the requested file transfers.
   - Display real-time statistics, including speed and success rates.

---

## **Usage Example**

### **Server Output**
```
Starting server...
Broadcasting offer...
Server listening on TCP port 12345
Valid UDP request from 192.168.1.2: 102400 bytes
Sent segment 1/100 to 192.168.1.2
...
```

### **Client Output**
```
Listening for server offers...
Offer received from 192.168.1.1: UDP Port 13117, TCP Port 12345
Enter file size (bytes): 102400
Enter number of TCP connections: 1
Enter number of UDP connections: 2

TCP 1: 100%|████████████████████████████████████████████| 102k/102k [00:02<00:00, 51.2kB/s]
TCP 1 Complete: Time: 2.05s, Speed: 50.0 bits/s

UDP 1: 100%|████████████████████████████████████████████| 102k/102k [00:01<00:00, 78.3kB/s]
UDP 1 Complete: Time: 1.55s, Speed: 72.3 bits/s, Success Rate: 97.5%

Real-Time Stats: Speed: 58.45 bits/s, Bytes Transferred: 204800
All transfers complete.
```

---

## **Testing**

### **Manual Tests**
1. **Basic Connectivity**:
   - Ensure the client detects server broadcasts.
2. **File Transfer**:
   - Test with different file sizes (e.g., 1 KB, 10 MB, 1 GB).
3. **Concurrent Connections**:
   - Run multiple TCP and UDP connections simultaneously.
4. **Edge Cases**:
   - Test with zero, negative, or excessively large file sizes.
   - Simulate packet loss for UDP transfers.

---

## **Customization**

### **Adjust Ports**
- Modify default ports in `shared.py`:
  ```python
  DEFAULT_UDP_PORT = 13117
  DEFAULT_TCP_PORT = 12345
  ```

### **Buffer Size**
- Change buffer size in `shared.py` for performance tuning:
  ```python
  BUFFER_SIZE = 1024  # Default: 1 KB
  ```

---

## **Known Limitations**
- **UDP Retransmissions**:
  - No retransmission for lost packets (can be added as an enhancement).
- **Server Load**:
  - Performance may degrade under extremely high concurrency.

---

## **Future Enhancements**
1. **Data Integrity**:
   - Add CRC or checksum validation for UDP packets.
2. **Retry Mechanism**:
   - Implement retransmissions for lost UDP packets.
3. **Cross-Platform Compatibility**:
   - Ensure seamless operation across different networks and environments.
4. **Graphical Output**:
   - Add a dashboard or real-time graph for monitoring.

---

## **Contributors**
- Ori Adika
- Idan Goldberg

---

Feel free to reach out if you have questions or suggestions. Happy coding! 🎉
