import random
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

connections = 0
while True:
    rand = random.randint(0, 10)
    message, address = serverSocket.recvfrom(1024)
    connections += 1
    response = 'msg' + str(connections) + ': ' + str(message)
    serverSocket.sendto(str.encode(response), address)
