import sys
from socket import *
import re



host = str(sys.argv[1])
port = int(sys.argv[2])

html_head=b'HTTP/1.1 200 OK\r\n\r\n'

not_found_head = b'HTTP/1.1 404 Not Found\r\n\r\n'
not_found = b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(100)
print("The server is ready to receive")
while 1:
    connectionSocket, addr = serverSocket.accept()
    try:
        request = connectionSocket.recv(1024)
        request = request.decode()
        src = str(request.split(' ')[1])
        #print('Here Is Request:\n',request)
        src = request.split()[1].encode()
        #print('src:',src[1:])
        e_file = src[1:].decode()
        #print('e_file:', e_file)
        #if e_file == 'index.html' or e_file == 'myimage.png':
        #    print('Here Is Request:\n',request)
        file = open(src[1:],'rb')
        print('Here Is Request:\n',request)
        print('*****************')
        #print('!!!!')
        #file = open(src[1:],'rb')
        index_content = html_head + file.read()
        file.close()
        connectionSocket.sendall(index_content)
        connectionSocket.close()
        
    except:
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')
        connectionSocket.close()
    connectionSocket.close()



