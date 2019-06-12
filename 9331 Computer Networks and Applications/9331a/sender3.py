#*************************************
# 9331 Simple Transport Protocol (STP)
#
# Sender:
#*************************************

from socket import *
from random import *
import random
import time
import sys
import pickle
import threading

# (14) arguments:  
# 6 arguments
# receiver_host_ip, receiver_port, file.pdf, 
# MWS, MSS, gamma, 
# 8 arguments are used exclusively by the PLD module:
# pDrop, pDuplicate, pCorrupt, maxOrder, pDelay, maxDelay
# seed


# set global:
global receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop, duplicated,pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed
global seq_num,ack_num,stp_closed_state,stp_syn_sent,stp_ack_sent,state_established,state_end



class Send_Thread (threading.Thread):
	def __init__(self,name):
		threading.Thread.__init__(self)
		self.addr = (receiver_host_ip,int(receiver_port))
		self.data = None
		self.name = name

	# create UDP socket
	sender_socket = socket(AF_INET,SOCK_DGRAM)
	#sender_socket.settimeout(1)
	#read file to data
	def read_data(self):
		with open(file,'r') as f:
			data = f.read()
		self.data = data
		return data

	def get_total_packet_num(self,data):
		size = len(data)
		num_packet = size//MSS
		if (size%MSS!=0):
			num_packet = num_packet + 1
		return num_packet

	def split_data(self,data,data_progress):
		size = len(data)
		end = data_progress + MSS 
		if end < size:
			payload = data[data_progress:end]
		else:
			payload = data[data_progress:size]

		return payload
	# send segment
	def send_data(self,packet):
		self.sender_socket.sendto(pickle.dumps(packet),self.addr)

	def recv_data(self):
		data,addr = self.sender_socket.recvfrom(2048)
		recv_packet = pickle.loads(data)
		return recv_packet

	def stp_SYN(self,seq_num,ack_num):
		print('stp: SYN')
		SYN = STP_Packet('',seq_num,ack_num,ack=False, syn = True, fin = False)
		return SYN

	def stp_ACK(self,seq_num,ack_num):
		print('stp: ACK')
		ACK = STP_Packet('',seq_num,ack_num,ack=True, syn = False, fin = False)
		return ACK

	# FIN
	def stp_FIN(self,seq_num,ack_num):
		print('stp: FIN')
		FIN = STP_Packet('',seq_num,ack_num,ack=False, syn = False, fin = True)
		return FIN

	# close socket
	def close_socket(self):
		self.sender_socket.close()

	# packet retransmit
	def retransmit(self,packet):
		self.sender_socket.sendto(pickle.dumps(packet),self.addr)
		self.update_log("snd", 'D',packet)
		print(':::: R_seq: {}'.format(packet.seq_num))

	# Record time
	def start_timer(self):
		self.start_time = time.clock() * 1000
		return self.start_time
	
	def current_time(self):
		self.current_time = time.clock() * 1000
		return self.current_time

	def previous_time(self):
		self.previous_time = time.clock() * 1000
		return self.previous_time

	def update_log(self,event,type,packet):
		seq_num = packet.seq_num
		ack_num = packet.ack_num
		size = len(packet.data)

		record_time = time.clock()
		record_time = round(record_time,3)
		record = event +' '+str(record_time)+' '+type+' '+str(seq_num)+' '+str(size)+' '+str(ack_num)+'\n'

		# write in log
		file = open("Sender_log.txt",'a+')
		file.write(record)
		file.close()

	def run(self):
		print("Starting: " + self.name)

		seq_num = 0
		ack_num = 0
		stp_closed_state = True
		stp_syn_sent = False
		stp_ack_sent = False
		# if 3-way-handshake complete, state_conn_established should be True
		state_established = False
		state_end = False

		previous_time = 0

		previous_packet = None

		stp_data = self.read_data()
		data_progress = 0
		length_data = len(stp_data)
		print('Data length: {}'.format(length_data))
		print('Total paket number: ', self.get_total_packet_num(stp_data))
		
		timeoutInterval = 0.5 + gamma * 0.25
		#timeoutInterval = 0.39
		
		sendbase = 0
		# pdrop is random number
		curr_time = 0

		num_transmitted=0
		num_retransmitted=0
		num_dropped = 0

		print('Loop:')
		number_loop=0
		num_reording = 0
		re_ordering_list = []
		num_reording = 0
		re_ordering_list = []

		while True:
			print('***** number of loop: {} *****'.format(number_loop))
			number_loop = number_loop+1
			# if the connection is closed, need to create connection and send SYN
			if stp_closed_state == True:
				print('***** State: closed. Ready to send SYN *****')
				#Sender first send the syn to connect
				syn_packet = self.stp_SYN(seq_num,ack_num)
				self.send_data(syn_packet)
				self.update_log("snd", 'SYN',syn_packet)
				stp_closed_state = False
				stp_syn_sent = True
				print('***** State: Connected *****')
			# if SYN has been sent:
			if stp_syn_sent == True:
				print('***** State: SYN has been sent *****')
				# get the ack
				syn_ack_packet = self.recv_data()
				if syn_ack_packet.ack == True and syn_ack_packet.syn == True:
					# syn and ack are all True, log update
					ack_num = syn_ack_packet.seq_num + 1
					self.update_log("rcv", 'SA',syn_ack_packet)

					#send ACK
					seq_num = seq_num + 1
					ack_packet = self.stp_ACK(seq_num,ack_num)
					self.send_data(ack_packet)
					self.update_log("snd", 'ACK',ack_packet)
					# 3-way-handshake complete
					state_established = True
					stp_syn_sent = False
					stp_ack_sent = True
					print('3-way-handshake complete')

			if state_established == True:
				print('***** State: connection established, start transfer file *****')
				payload = self.split_data(stp_data,data_progress)
				packet = STP_Packet(payload,seq_num,ack_num,ack=False,syn=False,fin=False)


				self.send_data(packet)
				#previous_packet = packet
				print('<< Packet send suceessfully >>')
				print(':::: seq: {}'.format(packet.seq_num))
				#not_acked_num = not_acked_num + 1
				#nextSeqNum = nextSeqNum + length(data)
				seq_num =  seq_num + len(payload)
				self.update_log('snd','D',packet)
				num_transmitted = num_transmitted + 1
				if curr_time == 0:
					curr_time = self.current_time()

				data_progress += len(payload)
				# transfer successfully
				print('State: wait for ack')
				#ack_packet = self.recv_data()
				#self.update_log("rcv", 'ACK', ack_packet)
				#num_acked = num_acked + 1
				#ack_num = ack_num + len(ack_packet.data)


				if data_progress == length_data :
					# client send fin to receiver to close
					fin_packet = self.stp_FIN(seq_num,ack_num)
					self.send_data(fin_packet)
					self.update_log('snd','FIN',fin_packet)
					state_end = True
					state_established = False
					print('test!')

				if state_end == True :
					print('End the connection:')
					# get ack packet from receiver
					ack_packet = self.recv_data()
					print('ACK is: {}'.format(ack_packet.ack_num))
					print('SEQ is: {}'.format(ack_packet.seq_num))
					if ack_packet.ack == True:
						fin_packet = self.recv_data()
						print('ACK is: {}'.format(fin_packet.ack_num))
						print('SEQ is: {}'.format(fin_packet.seq_num))
						print(fin_packet.fin)
						self.update_log("rcv", 'FA',fin_packet)
						if fin_packet.fin == True:
							ack_num = ack_num + 1
							# send ACK
							ack_packet = self.stp_ACK(seq_num,ack_num)
							self.send_data(ack_packet)
							self.update_log("snd", 'ACK',ack_packet)
							print("Waiting 5 seconds")
							time.sleep(1)
							break
		self.close_socket()



class Receive_Thread (threading.Thread):
	def __init__(self,name):
		threading.Thread.__init__(self)
		self.addr = (receiver_host_ip,receiver_port)
		self.data = None
		self.name = name
	
	# create UDP socket
	sender_socket = socket(AF_INET,SOCK_DGRAM)
	#sender_socket.settimeout(1)

	# receive data from server
	def recv_data(self):
		data,addr = self.sender_socket.recvfrom(2048)
		recv_packet = pickle.loads(data)
		return recv_packet

	def read_data(self):
		with open(file,'r') as f:
			data = f.read()
		self.data = data
		return data

	def stp_SYN(self,seq_num,ack_num):
		print('stp: SYN')
		SYN = STP_Packet('',seq_num,ack_num,ack=False, syn = True, fin = False)
		return SYN

	def stp_ACK(self,seq_num,ack_num):
		print('stp: ACK')
		ACK = STP_Packet('',seq_num,ack_num,ack=True, syn = False, fin = False)
		return ACK

	# FIN
	def stp_FIN(self,seq_num,ack_num):
		print('stp: FIN')
		FIN = STP_Packet('',seq_num,ack_num,ack=False, syn = False, fin = True)
		return FIN

	# close socket
	def close_socket(self):
		self.sender_socket.close()

	def update_log(self,event,type,packet):
		seq_num = packet.seq_num
		ack_num = packet.ack_num
		size = len(packet.data)

		record_time = time.clock()
		record_time = round(record_time,3)
		record = event +' '+str(record_time)+' '+type+' '+str(seq_num)+' '+str(size)+' '+str(ack_num)+'\n'

		# write in log
		file = open("Sender_log.txt",'a+')
		file.write(record)
		file.close()
	def run(self):

		print("Starting: "+self.name)
		stp_data = self.read_data()
		length_data = len(stp_data)
		print('RRRRR:   Data length: {}'.format(length_data))
		now_time = []
		while True:	
			if state_established == True:
				print('State: wait for ack')
				ack_packet = self.recv_data()
				sender.update_log("rcv", 'ACK', ack_packet)
				#num_acked = num_acked + 1
				#ack_num = ack_num + len(ack_packet.data)
			if state_end == True:
				now_time.append(time.time())

			if int(now_time[-1]-now_time[0]) == 5:
				break
				

		self.close_socket()






class STP_Packet:
	def __init__(self,data,seq_num,ack_num,ack = False, syn = False, fin = False,checksum = None):
		self.data = data
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack = ack
		self.syn = syn
		self.fin = fin
		self.checksum = checksum





if __name__ =='__main__':
	# give value and ready to start
	# set global :
	receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop,duplicated,pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed = sys.argv[1:]
	print('Host: {}\nPort: {}\nFile: {}\nMWS: {}\nMSS: {}\ngamma: {}\npdrop: {}\nduplicated: {}\npCorrupt: {}\npOrder: {}\nmaxOrder: {}\npDelay: {}\nmaxDelay: {}\nseed: {}\n'
		.format(receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop, duplicated,
		pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed))


	MWS = int(MWS)
	MSS = int(MSS)
	gamma = int(gamma)
	pdrop = float(pdrop)
	duplicated = float(duplicated)
	pCorrupt = float(pCorrupt)
	pOrder = float(pOrder)
	maxOrder = int(maxOrder)
	pDelay = float(pDelay)
	maxDelay = int(maxDelay)
	seed = int(seed)

	seq_num = 0
	ack_num = 0

	random.seed(int(seed))


	previous_time = 0

	previous_packet = None
	Delay_packet = None

	stp_closed_state = True
	stp_syn_sent = False
	stp_ack_sent = False
	# if 3-way-handshake complete, state_conn_established should be True
	state_established = False
	state_end = False
	#file = open("Sender_log.pdf","w")
	#file.close()
	not_acked_num = 0
	sendbase = 0


	#num_transmitted=0
	num_retransmitted=0
	num_dropped = 0

	# Start Sender class
	print('TWO THREAD:')
	send_thread = Send_Thread('send_thread')
	recv_thread = Receive_Thread('recv_thread')

	# start thread
	send_thread.start()
	recv_thread.start()
























