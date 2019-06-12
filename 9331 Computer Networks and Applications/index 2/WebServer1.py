import sys
from socket import *


#host = str(sys.argv[1])
#port = 8080 #int(sys.argv[1]) # change this port number if required
#host = ''


host = str(sys.argv[1])
port = int(sys.argv[2])

html_head='''
HTTP/1.x 200 ok
Content-Type: text/html

'''
image_head='''
HTTP/1.x 200 ok
Content-Type: image/png

'''

not_found = '''
HTTP/1.1 404 Not Found
404 Not Found\n
404 Not Found
'''


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(100)
print("The server is ready to receive")
while 1:
    connectionSocket, addr = serverSocket.accept()
    try:
        request = connectionSocket.recv(1024)
        print('Here Is Request:\n',request)
        src = request.split()[1]
        print('file:',src)
        file = open(src[1:],'rb')
        content = file.read()
        connectionSocket.send(b'HTTP/1.1 200 OK\r\n\r\n')
        connectionSocket.sendall(content)
    except IOError:
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')
        connectionSocket.close()

connectionSocket.close()  
    



