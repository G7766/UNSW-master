#UDP

from socket import *
import time

serverPort = 8080 # change this port number if required
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))   #serverSocket.bind(('', serverPort))  ''位置填写主机地址，默认主机地址
print("The server is ready to receive")
while 1:
    sentence,addr= serverSocket.recvfrom(1024)      #1024 BUFSIZE
    capitalizedSentence = sentence.upper()
    time.sleep(1)
    serverSocket.sendto(capitalizedSentence,addr)

serverSocket.close()