#*************************************
# 9331 Simple Transport Protocol (STP)
#
# Receiver:
#*************************************

from socket import *
from random import *
import time
import sys
import pickle
from collections import Counter
# (14) arguments:  
# 6 arguments
# receiver_host_ip, receiver_port, file.pdf, 
# MWS, MSS, gamma, 
# 8 arguments are used exclusively by the PLD module:
# pDrop, pDuplicate, pCorrupt, maxOrder, pDelay, maxDelay
# seed
import hashlib
def get_token(payload):
    md5str = payload
  #生成一个md5对象
    m1 = hashlib.md5()
  #使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token

class STP_Packet:
	def __init__(self,data,seq_num,ack_num,ack = False, syn = False, fin = False,checksum = None):
		self.data = data
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack = ack
		self.syn = syn
		self.fin = fin
		self.checksum = checksum


class Receiver:
	# create sender side data
	def __init__(self, port,file):
		self.port = int(port)
		self.file = file

	# create UDP socket
	receiver_socket = socket(AF_INET,SOCK_DGRAM)
	#receiver_socket.settimeout(1)

	#def add_payload(self,data):
	#	with open("r_test.txt",'a+') as f:
	#		f.write(data)

	# receive data from server
	def read_data(self):
		with open(self.file,'rb') as f:
			data = f.read()
		return data
	def recv_data(self):
		#print('Receive data:')
		data,addr = self.receiver_socket.recvfrom(2048)
		recv_packet = pickle.loads(data)
		return recv_packet,addr
	
	# send segment
	def send_data(self,packet,addr):
		self.receiver_socket.sendto(pickle.dumps(packet),addr)


	def stp_SYNACK(self,seq_num,ack_num):
		print('stp: SYNACK')
		SYNACK = STP_Packet('',seq_num,ack_num,ack=True, syn = True, fin = False)
		return SYNACK

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
		print('Connection closed')
		self.receiver_socket.close()

	def update_log(self,event,type,packet):
		seq_num = packet.seq_num
		ack_num = packet.ack_num
		size = len(packet.data)

		record_time = time.clock()
		record_time = round(record_time,3)
		record = event +' '+str(record_time)+' '+type+' '+str(seq_num)+' '+str(size)+' '+str(ack_num)+'\n'

		# write in log
		file = open("Receiver_log.txt",'a+')
		file.write(record)
		file.close()

def count_dup(q):
	z = Counter(q)
	#print(z)
	k = 0
	for i in z:
		if z[i] > 1:
			k= k + 1
	#print(k)
	return k

if __name__ =='__main__':
	# give value and ready to start
	host,port, file = sys.argv[1:]
	print('Host: {}\nPort: {}\nFile: {}\n'
		.format(host,port,file))

	# set seq and ack
	seq_num = 0
	ack_num = 0
	next_seq_num = 0
	next_ack_num = 0

	# receiver state
	state_listen = True
	state_established = False
	state_end = False
	r_syn_receive = False
	r_synack_sent = False

	# sender address
	sender_addr = None


	receiver = Receiver(port, file)
	receiver.receiver_socket.bind(('',receiver.port))
	# the progress of file has already been sent
	data_progress = 0
	# stp buffer
	stp_buffer = {}
	stp_data = receiver.read_data()
	length_data = len(stp_data)
	total_seg = 0
	num_error = 0
	num_segment = 0
	ack_list =[]
	l =[]
	ll = []
	flag = 0
	print('Loop Start. Receiver is ready....')
	number_loop = 0
	while True:
		print(' *****> number of loop: {}'.format(number_loop))
		number_loop = number_loop + 1

		# if the connection is closed, need to create connection and send SYN
		if state_listen == True:
			print(' ===========> State: LISTEN. Ready to send listen')
			#Sender first send the syn to connect
			syn_packet, sender_addr = receiver.recv_data()
			total_seg = total_seg + 1
			receiver.update_log("rcv", 'S', syn_packet)
			# acknowledge Sender SYN
			ack_num = ack_num + 1
			# sending  SYNACK
			if syn_packet.syn == True:
				synack_packet = receiver.stp_SYNACK(seq_num,ack_num)
				receiver.send_data(synack_packet,sender_addr)
				receiver.update_log("snd", 'S', synack_packet)
				seq_num = seq_num + 1
				r_synack_sent = True
				state_listen = False

		# if SYNACK has been sent wait for ack:
		if r_synack_sent == True:
			print(' ===========> State: SYNACK has been sent')
			# ready to get the ack
			ack_packet,sender_addr = receiver.recv_data()
			total_seg = total_seg + 1
			receiver.update_log("rcv", 'A', ack_packet)

			if ack_packet.ack == True:
				# ack is True
				state_established = True
				r_synack_sent = False
				# 3-way-handshake complete
				print('3-way-handshake complete')
				#break



		# Handshake established 
		# send the payload data segemnts util the file is transfered
		if state_established == True:
			print(" state: connection established")
			# receive packet until FIN close
			while True:
				packet, sender_addr = receiver.recv_data()
				total_seg = total_seg + 1
				num_segment = num_segment + 1
				'''
				for i in l[:-2]:
					if i == len(packet.data)
					pass
				else:
					ack_num = ack_num + len(packet.data)
				'''
				if packet.checksum!=None:
					if get_token(packet.data)!= get_token(packet.checksum):
						print('Packet corrupt!')
						num_error = num_error + 1
						packet, sender_addr = receiver.recv_data()
						total_seg = total_seg + 1
						num_segment = num_segment + 1
						print(len(packet.data))
				print(packet.seq_num)
				print(packet.ack_num)
				print(len(packet.data))

				l.append(packet.seq_num)
				if len(l)>=2:
					for i in l[:-1]:
						if i == packet.seq_num:
							flag = 1
							break
					if flag != 1:
						ack_num = ack_num + len(packet.data)
					else:
						flag = 0
				else:			
					ack_num = ack_num + len(packet.data)
					#ll.append(ack_num)


				ack_list.append(ack_num)
				print(packet.seq_num)
				# if get FIN
				# close receving

				# checksum:

				if packet.fin == True:
					print('FIN initiated by sender . . .')
					receiver.update_log('rcv','F',packet)
					state_end = True
					state_established = False
					break
				# otherwise
				elif packet.seq_num == seq_num:
					print("Normal packet, send ack")
					#ack_num = ack_list[0]
					#ack_list.pop(0)
					ack_packet = receiver.stp_ACK(seq_num, ack_num)
					receiver.send_data(ack_packet,sender_addr)
					receiver.update_log('snd','A',ack_packet)
					seq_num = seq_num+len(packet.data)
					#receiver.add_payload(packet.data)
					receiver.update_log('rcv','D',packet)
				else:
					print('Add in buffer.')
					ack_packet = receiver.stp_ACK(seq_num, ack_num)
					receiver.send_data(ack_packet,sender_addr)
					receiver.update_log('drop','A',ack_packet)
					stp_buffer[packet.seq_num] = packet

		

		# if state_end True, close connection
		if state_end == True:
			print('End of connection')
			ack_num = ack_num+1
			# send ACK + FIN to the sender
			ack_packet = receiver.stp_ACK(seq_num,ack_num)
			receiver.send_data(ack_packet,sender_addr)
			print('test1')
			fin_packet = receiver.stp_FIN(seq_num, ack_num)
			receiver.send_data(fin_packet,sender_addr)
			receiver.update_log("snd", 'F', fin_packet)
			print('test2')
			# and then wait for feedback(ACK)
			ack_packet,sender_addr = receiver.recv_data()
			total_seg = total_seg + 1
			receiver.update_log("rcv", 'A', ack_packet)

			# receive sender ack, close.
			print('end')
			if ack_packet.ack == True:
				receiver.close_socket()
				break

	#receiver.close_socket()
	#print(l)
	#print(ll)

	dup_ack = count_dup(l)

	print('STP CLOSE')

	line = "========================================\n"
	file = open('Sender_log.txt','a+')
	data = "Amount of Data Received = {} bytes\n".format(length_data)
	total_seg = "Total segments received = {}\n".format(total_seg)
	Data_seg = "Data segments received = {}\n".format(num_segment)
	error_Data = "Data Segments with bit errors = {}\n".format(num_error)
	dup_seg = "Duplicate data segments received  = {}\n".format(dup_ack)
	dup_ack_sent = "Duplicate Acks sent = {}\n".format(dup_ack)

	file = open('Receiver_log.txt','a+')
	final_str = "\n"+line + data + total_seg +Data_seg+ error_Data + dup_seg + dup_ack_sent +line
	file.write(final_str)
	file.close()
























