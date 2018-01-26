import math
from socket import *

def is_prime(val):
    for i in range(2, int(math.sqrt(val) + 1)):
        if (val % i) == 0:
            return False
    return True

def nth_prime(n):
    i = 0
    val = 2
    while i < n:
        if is_prime(val):
            i += 1
            if i == n:
                return val
        val += 1

def main():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', 12000))

    print("Server On")
    while True:
        message, address = serverSocket.recvfrom(1024)

        print("Message from", address, ":", message)

        # n =  re.sub("[^0-9]", "", str(message))
        n = str(message)[2:-1]
        prime = nth_prime(int(n))

        response = str(prime)
        serverSocket.sendto(str.encode(response), address)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer Off")
