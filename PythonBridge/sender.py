import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    sock.sendto(b"HELLO", ("127.0.0.1", 7001))
    print("sent")