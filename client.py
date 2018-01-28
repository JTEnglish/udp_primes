import time
from socket import *

def main():
    print("Msg\tResult\tTime (ms)")
    for val in range(1, 250):
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(1)
        message = str.encode(str(val))
        addr = ("127.0.0.1", 12000)

        start = time.time()
        clientSocket.sendto(message, addr)
        try:
            data, server = clientSocket.recvfrom(1024)
            data = str(data)[2:-1]
            end = time.time()
            elapsed = end - start
            print('%d\t%s\t%f' % (val, data, elapsed))
        except timeout:
            print('REQUEST TIMED OUT')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer Off")
