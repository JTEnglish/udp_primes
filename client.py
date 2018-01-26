import time
from socket import *

for ping in range(10):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    message = str.encode(str(ping))
    addr = ("127.0.0.1", 12000)

    start = time.time()
    clientSocket.sendto(message, addr)
    try:
        data, server = clientSocket.recvfrom(1024)
        end = time.time()
        elapsed = end - start
        print('%s %d %d' % (data, ping, elapsed))
    except timeout:
        print('REQUEST TIMED OUT')
