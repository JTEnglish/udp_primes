import time
from socket import *

def main():
    print("Msg\tTime\tResult")
    for ping in range(1, 100):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(1)
        message = str.encode(str(ping))
        addr = ("127.0.0.1", 12000)

        start = time.time()
        clientSocket.sendto(message, addr)
        try:
            data, server = clientSocket.recvfrom(1024)
            data = str(data)[2:-1]
            end = time.time()
            elapsed = end - start
            print('%d\t%d\t%s' % (ping, elapsed, data))
        except timeout:
            print('REQUEST TIMED OUT')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer Off")
