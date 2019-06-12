# Python 3.6

# 10message
# client wait up to 1 second for a reply
# if no reply is received, assume taht packet was lost
# client send message, reply was received or not , send again..
# sequence_number starts at 0 and progresses to 9
# function to read system time in millliseconds
# The RTT value should be printed to the standard output 
# show the timeout requests in the out put
#  replace the 'rtt=120ms' in the above example with 'time out'
#  report the minimum, maximum and the average RTTs of all packets 
#  --- received successfully at the end of your program's output.


#command python PingClient.py host port


import sys
import time
total = len(sys.argv)
cmdargs = str(sys.argv)

from socket import *

def avg(l):
	length = len(l)
	z=0
	for i in l:
		z = z+i

	return z/length


address = str(sys.argv[1]);
port = int(sys.argv[2]) #change this port number if required
ADDR=(address,port)
clientSocket = socket(AF_INET, SOCK_DGRAM)
#clientSocket.connect((address, port))
clientSocket.settimeout(1) #settimeout: time over 1 seconds, break
i=0
rtt_time=[]
while i!=10:
	try:
		#message = input('Input lowercase sentence:')   # change raw_input to input
		message = "PING {} {} ".format(i,int(time.time()))
		time1=time.time()
		clientSocket.sendto(message.encode(),ADDR)	#add encode
		ReceiveMessage = clientSocket.recvfrom(1024)
		time2=time.time()
		print('PING to {}, seq = {} rtt = {:.2f} ms.'.format(address, i, (time2-time1)*1000))
		time.sleep(1)
		rttT = (time2-time1)*1000
		rtt_time.append(rttT)
		i=i+1
	except Exception:
		print('PING to {}, seq = {} time out.'.format(address, i))
		i=i+1
		continue

#print(rtt_time)
print('The minimum RTTs: {:.2f} ms;\nThe maximum RTTs: {:.2f} ms;\nThe average RTTs: {:.2f} ms;'
	.format(min(rtt_time), max(rtt_time), avg(rtt_time)))
clientSocket.close()


