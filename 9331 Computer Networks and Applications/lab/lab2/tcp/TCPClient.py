import sys
from socket import *
total = len(sys.argv)
cmdargs = str(sys.argv)

host = str(sys.argv[1])
port = int(sys.argv[2]) #change this port number if required

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, port))
sentence = input('Input lowercase sentence:')   # change raw_input to input
clientSocket.send(sentence.encode())          #add encode
receivedSentence = clientSocket.recv(1024)
print('From Server:', receivedSentence)
clientSocket.close()
