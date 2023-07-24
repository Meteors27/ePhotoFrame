import socket
import os

# If we're on a Raspberry Pi Pico, we need to set up the WiFi AP
if str(os.uname()).find("rp2") > -1:
    import network

    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid="ePaper", password="88888888")
    wlan.active(True)
    print("WiFi AP started")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.getaddrinfo("127.0.0.1", 9000)[0][-1]  # TODO: change to  0.0.0.0
s.bind(addr)
s.listen(1)
print("Listening on", addr)
conn, addr = s.accept()
print("Connected by", addr)
while True:
    data = conn.recv(1024)
    if not data:
        break
    # process data
    print(data)

conn.close()
