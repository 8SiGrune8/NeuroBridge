import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 7001))

print("Listening on 7001...")

while True:
    data, addr = sock.recvfrom(4096)
    print("Received:", data)