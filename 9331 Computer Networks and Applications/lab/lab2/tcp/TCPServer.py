import sys
from socket import *

#host = str(sys.argv[1])
port = int(sys.argv[1]) # change this port number if required
host = ''
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
print("The server is ready to receive")
while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    ChangeSentence = sentence.upper()
    connectionSocket.send(ChangeSentence)
    connectionSocket.close()

