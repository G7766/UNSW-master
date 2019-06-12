import sys
from socket import *
import re

#host = str(sys.argv[1])
#port = 8080 #int(sys.argv[1]) # change this port number if required
#host = ''


host = str(sys.argv[1])
port = int(sys.argv[2])

head_content='''
HTTP/1.x 200 ok
Content-Type: text/html

'''
image_content='''
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
    request = connectionSocket.recv(1024)
    #requestHeaderLines = request.splitlines()
    #print(request)
    request = request.decode()
    print('Here Is Request:\n',request)
    method = request.split(' ')[0]
    #src = request.split(' ')[1]
    #print('Connect by: ', addr)
    #print('Request is:\n',request)
    if method == 'GET': 
        try:
        	src = request.split(' ')[1]
        	if src == '/index.html':
        		file = open('index.html','r')
        		index_content = head_content + file.read()
        		print('Here is index_content: \n',index_content)
        		file.close()
        		content = index_content
        	elif src =='/myimage.png':
        		file = open('myimage.png','rb')
        		image_content = image_content.encode() + file.read()
        		print('Here is image_content: \n',image_content)
        		file.close()
        		content = image_content
        	else:
        		content = not_found
        		print('404 Not Found')
        except:
        	print('404 Not Found')
        	content = not_found
        	#content = content.encode()
    #if method == 'POST': 
    if src =='/myimage.png':
    	connectionSocket.sendall(content)
    	connectionSocket.close()
    else:
    	print('***')
    	connectionSocket.sendall(content.encode())
    	connectionSocket.close()


