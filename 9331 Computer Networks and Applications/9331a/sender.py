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

# (14) arguments:  
# 6 arguments
# receiver_host_ip, receiver_port, file.pdf, 
# MWS, MSS, gamma, 
# 8 arguments are used exclusively by the PLD module:
# pDrop, pDuplicate, pCorrupt, maxOrder, pDelay, maxDelay
# seed

class STP_Packet:
	def __init__(self,data,seq_num,ack_num,ack = False, syn = False, fin = False):
		self.data = data
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack = ack
		self.syn = syn
		self.fin = fin

class Sender:
	# create sender side data
	def __init__(self, _host_ip, _port, file, MWS, MSS, gamma,pdrop, duplicated,
		pCorrupt,pOrder,maxOrder,maxDelay,seed):
		self._host_ip = _host_ip
		self._port = int(_port)
		self.addr = (self._host_ip,self._port)
		self.file = file
		self.MWS = int(MWS)
		self.MSS = int(MSS)
		self.gamma = int(gamma)
		self.current_time = 0
		self.previous_time =0
		self.start_time = 0
		# PLD :
		self.pdrop = float(pdrop)
		self.duplicated = float(duplicated)
		self.pCorrupt = float(pCorrupt)
		self.pOrder = float(pOrder)
		self.maxOrder = int(maxOrder)
		self.maxDelay = 1000 * int(maxDelay)
		random.seed(int(seed))
		self.random = random.random()
		#self.data =0

	# create UDP socket
	sender_socket = socket(AF_INET,SOCK_DGRAM)
	#sender_socket.settimeout(1)

	#read file to data
	def read_data(self):
		with open(self.file,'r') as f:
			data = f.read()
		return data
	def split_data(self,data,data_progress):
		size = len(data)
		end = data_progress + self.MSS 
		if end < size:
			payload = data[data_progress:end]
		else:
			payload = data[data_progress:size]

		return payload
	# send segment
	def send_data(self,packet):
		self.sender_socket.sendto(pickle.dumps(packet),self.addr)

	# receive data from server
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
		sender.update_log('r_snd','D',packet)

	# Record time
	def start_timer(self):
		self.start_time = time.clock() * 1000
	
	def current_time(self):
		self.current_time = time.clock() * 1000

	def store_time(self):
		self.previous_time = time.clock() * 1000

	def update_log(self,packet):
		seq_num = packet.seq_num
		ack_num = packet.ack_num
		size = len(packet.data)

		record_time = time.clock() * 1000
		record = str(record_time)+' '+str(seq_num)+' '+str(size)+' '+str(ack_num)+'\n'

		# write in log
		file = open("Sender_log.txt",'a+')
		file.write(record)
		file.close()

	# PLD module:

	def PLD_pdrop(self):
		r = self.random
		if r > self.pdrop:
			return False
		return True
	def PLD_pDuplicate(self):
		r = self.random
		if r > self.duplicated:
			return False
		return True
	def PLD_pCorrupt(self):
		r = self.random
		if r > self.pCorrupt:
			return False
		return True
	def PLD_pOrder(self):
		r = self.random
		if r > self.pOrder:
			return False
		return True
	def PLD_pDelay(self):
		r = self.random
		if r > self.pDelay:
			return False
		return True


if __name__ =='__main__':
	# give value and ready to start
	receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop,duplicated,pCorrupt,pOrder,maxOrder,maxDelay,seed= sys.argv[1:]
	print('Host: {}\nPort: {}\nFile: {}\nMWS: {}\nMSS: {}\ngamma: {}\npdrop: {}\nduplicated: {}\npCorrupt: {}\npOrder: {}\nmaxOrder: {}\nmaxDelay: {}\nseed: {}\n'
		.format(receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop, duplicated,
		pCorrupt,pOrder,maxOrder,maxDelay,seed))
	seq_num = 0
	ack_num = 0
	stp_closed_state = True
	stp_syn_sent = False
	stp_ack_sent = False
	# if 3-way-handshake complete, state_conn_established should be True
	state_established = False
	#file = open("Sender_log.pdf","w")
	#file.close()
	not_acked_num = 0
	sendbase = 0

	packet_not_acked_list = {}

	num_transmitted=0
	num_retransmitted=0
	num_dropped = 0

	# Start Sender class
	print('Sender Start:')
	sender = Sender(receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop,duplicated,pCorrupt,pOrder,maxOrder,maxDelay,seed)
	#a=int(seed)
	#print(a)
	#random.seed(a)
	#random = random.random()
	#sender.random = random
	print(sender.random )
	stp_data = sender.read_data()
	#with open("test1.txt",'r') as f:
	#	stp_data = f.read()


	# count packet number and unacked packets
	curr_packet_number = 0
	packet_info = {}

	# info of the data already send
	data_progress = 0
	length_data = len(stp_data)
	print('Data length: {}'.format(length_data))

	#TimeoutInterval
	#EstimatedRTT = 500 milliseconds 
	#DevRTT = 250 milliseconds
	#TimeoutInterval = EstimatedRTT + gamma * DevRTT =0.5+1 =1.5 s
	timeoutInterval = 0.5 + sender.gamma * 0.25
	sendbase = 0
	# pdrop is random number

	print('Loop:')
	number_loop=0
	# use for check PLD
	flag = 0
	while True:
		print('***** number of loop: {} *****'.format(number_loop))
		number_loop = number_loop+1

		# if the connection is closed, need to create connection and send SYN
		if stp_closed_state == True:
			print('***** State: closed. Ready to send SYN *****')
			#Sender first send the syn to connect
			syn_packet = sender.stp_SYN(seq_num,ack_num)
			sender.send_data(syn_packet)
			sender.update_log(syn_packet)
			stp_closed_state = False
			stp_syn_sent = True
			print('***** State: Connected *****')


		# if SYN has been sent:
		if stp_syn_sent == True:
			print('***** State: SYN has been sent *****')
			# get the ack
			syn_ack_packet = sender.recv_data()
			if syn_ack_packet.ack == True and syn_ack_packet.syn == True:
				# syn and ack are all True, log update
				ack_num = syn_ack_packet.seq_num + 1
				sender.update_log(syn_ack_packet)

				#send ACK
				seq_num = seq_num + 1
				ack_packet = sender.stp_ACK(seq_num,ack_num)
				sender.send_data(ack_packet)
				sender.update_log(ack_packet)
				# 3-way-handshake complete
				state_established = True
				stp_syn_sent = False
				stp_ack_sent = True
				print('3-way-handshake complete')

				#break
		#---------------------
		# established state
		#---------------------
		# send the payload data segemnts util the file is transfered
		if state_established == True:
			print('***** State: connection established, start transfer file *****')

			# check the previous packet has acked or not, 
			# if exists and over timeout time 
			# then retransmit:  (use not_acked_num)
			if not_acked_num !=0:
				print('Number unacked: {}'.format(not_acked_num))
				# find the smallest from current time packet not be sent
				# which is the smallest number in packet_not_acked_list
				oldest = 99999999
				for i in packet_not_acked_list:
					if oldest > i:
						oldest = i

				for i in packet_not_acked_list:
					if i == oldest:
						print("the oldest packet time is: {}".format(oldest))
						retrans_packet = packet_not_acked_list[oldest]
						print("the oldest packet seq_num: {}".format(retrans_packet.seq_num))

				# the time difference from previos time
				diff_time = sender.previous_time - sender.start_time
				print("oldest time = {}").format(sender.start_time)
				print("previous time = {}").format(sender.prev_time)
				print("time difference = {}").format(time_diff)
				print("timeout = {}").format(sender.gamma)


				# check if it reaches the timeout
				if diff_time > timeoutInterval:
					print("TIMEOUT !!! PACKET RETRANSMITTING")
					sender.retransmit(packet)
					not_acked_num = not_acked_num + 1
					seq_num = seq_num + len(payload)
					num_retransmitted = num_retransmitted + 1
					continue


			# create packet
			payload = sender.split_data(stp_data,data_progress)
			packet = STP_Packet(payload,seq_num,ack_num,ack=False,syn=False,fin=False)

			# packet not for connection
			#check PLD:
			# first check pdrop
			pld_pdrop_check = sender.PLD_pdrop()
			# not drop
			if pld_pdrop_check == False:
				# get the oldest unacknowledged segment
				# if timer currently not running :start running
				if sender.start_time == 0:
					sender.start_timer()
					print('Start time: {}\n'.format(sender.start_time))
				# pass segment to ip
				sender.send_data(packet)
				print('<< Packet send suceessfully >>')
				not_acked_num = not_acked_num + 1
				#nextSeqNum = nextSeqNum + length(data)
				seq_num =  seq_num + len(payload)
				sender.update_log(packet)
				num_transmitted = num_transmitted + 1
			# drop:
			else:
				print('Packet Drop!')
				sender.store_time()
				num_dropped = num_dropped+1
				sender.update_log(packet)
				# store drop packet and wait for retransmit
				packet_not_acked_list[sender.previous_time] = packet
				continue

			# transfer successfully
			data_progress = data_progress + len(payload)
			print('State: wait for ack')
			ack_packet = sender.recv_data()
			sender.update_log(ack_packet)
			ack_num = ack_num + len(ack_packet.data)

			if ack_packet.ack == True and ack_packet.ack_num > sendbase:
				print('<< Packet ACK RECEIVED >>')
				not_acked_num = not_acked_num - 1
				sendbase = ack_packet.ack_num
				if not_acked_num == 0:
					sender.start_timer()


			# 四次挥手
			'''
			（1）客户端A发送一个FIN，用来关闭客户A到服务器B的数据传送（报文段4）。
			（2）服务器B收到这个FIN，它发回一个ACK，确认序号为收到的序号加1（报文段5）。和SYN一样，一个FIN将占用一个序号。
			（3）服务器B关闭与客户端A的连接，发送一个FIN给客户端A（报文段6）。
			（4）客户端A发回ACK报文确认，并将确认序号设置为收到序号加1（报文段7）
			'''
			# the data progress equal to len of data(entire file)
			# the file is trinsfered complete, close connection
			if data_progress == length_data:
				# client send fin to receiver to close
				fin_packet = sender.stp_FIN(seq_num,ack_num)
				sender.send_data(fin_packet)
				sender.update_log(fin_packet)
				state_end = True
				state_established = False
		
		# if state_end is ture:
		if state_end == True:
			print('End the connection:')
			# get ack packet from receiver
			ack_packet = sender.recv_data()
			print('ACK is: {}'.format(ack_packet.ack_num))
			print('SEQ is: {}'.format(ack_packet.seq_num))
			if ack_packet.ack == True:
				fin_packet = sender.recv_data()
				print('ACK is: {}'.format(fin_packet.ack_num))
				print('SEQ is: {}'.format(fin_packet.seq_num))
				sender.update_log(fin_packet)

				if fin_packet.fin == True:
					ack_num = ack_num + 1
					# send ACK
					ack_packet = sender.stp_ACK(seq_num,ack_num)
					sender.send_data(ack_packet)
					sender.update_log(ack_packet)
					print("Waiting 5 seconds")
					time.sleep(5)
					break

	sender.close_socket()
	print('STP CLOSE')
	file = open('Sender_log.txt','a+')
	data = "Data Transferred = {} bytes\n".format(length_data)
	seg_sent = "Segments Sent = {}\n".format(num_transmitted)
	pkt_dropped = "Packets Dropped = {}\n".format(num_dropped)
	pkt_delayed = "Packets Delayed = N/A\n"
	seg_retrans = "Segments Retrans = {}\n".format(num_retransmitted)
	ack_duplicate = "Duplicate Acks = N/A"
	final_str = "\n" + data + seg_sent + pkt_dropped + pkt_delayed + seg_retrans + ack_duplicate
	file.write(final_str)
	file.close()























