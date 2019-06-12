from socket import *
from random import *
import random
import time
import sys
import pickle
from collections import Counter
import hashlib

#from reportlab.pdfgen import canvas
#设置绘画开始的位置

#def generate_pdf(c,data):
#    c.drawString(2, 800,data)

def get_token(payload):
    md5str = payload
    m1 = hashlib.md5()
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
	#def read_data(self):
	#	with open(self.file,'rb') as f:
	#		data = f.read()
	#	return data
	def recv_data(self):
		try:
			data,addr = self.receiver_socket.recvfrom(2048)
			recv_packet = pickle.loads(data)
			return recv_packet,addr
		except:
			return False
	
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
	file_r = file
	# receiver state
	state_listen = True
	state_established = False
	state_end = False
	r_syn_receive = False
	r_synack_sent = False

	# sender address
	sender_addr = None
	total_data = ''.encode()

	receiver = Receiver(port, file)
	receiver.receiver_socket.bind(('',receiver.port))
	# the progress of file has already been sent
	data_progress = 0
	# stp buffer
	stp_buffer = {}
	#stp_data = receiver.read_data()
	length_data = 0
	#length_data = len(stp_data)
	total_seg = 0
	num_error = 0
	num_segment = 0
	dup_ack_sent =0
	dup_ack =0
	ack_list =[]
	l =[]
	ll = []
	flag = 0
	previous_packet = None
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
			while True:
				packet, sender_addr = receiver.recv_data()
				#ack_num = ack_num + len(packet.data)
				# if corrupt
				if  packet.fin != True and get_token(str(packet.data))!= get_token(str(packet.checksum)):
					print('cccccccccccccc')
					#receiver.send_data(previous_packet,sender_addr)
					#print(previous_packet.seq_num,' ~~ ', previous_packet.ack_num)
					num_error +=1
					packet.seq_num = 1
					total_seg +=1
					num_segment +=1
					receiver.update_log('snd','D',packet)
					total_data = total_data + packet.checksum
					#time.sleep(0.1)
					continue
				
				#print(len(packet.data))
				if packet.seq_num in l:
					dup_ack_sent+=1
					continue
				else:
					l.append(packet.seq_num)
					dup_ack+=1
					ack_num = ack_num + len(packet.data)
					print(ack_num)
					
				try:
					if packet.fin == True:
						print('FIN initiated by sender . . .')
						receiver.update_log('rcv','F',packet)
						state_end = True
						state_established = False
						break
					elif packet.seq_num == seq_num:
						print('!!!!!!!')
						total_seg +=1
						packet.ack_num = 1
						total_data =total_data+ packet.checksum
						receiver.update_log('rcv','A',packet)
						ack_packet = receiver.stp_ACK(seq_num, ack_num)
						previous_packet = ack_packet
						ack_packet.seq_num = 1
						#previous_packet = ack_packet
						receiver.send_data(ack_packet,sender_addr)
						receiver.update_log('snd','D',ack_packet)
						seq_num = seq_num+len(packet.data)
						num_segment +=1
					else:
						print('Add to buffer')
				except:
					continue
		if state_end == True:
			print('End of connection')
			seq_num = 1 
			ack_num = ack_num + 1
			# send ACK + FIN to the sender
			ack_packet = receiver.stp_ACK(seq_num,ack_num)
			receiver.send_data(ack_packet,sender_addr)
			receiver.update_log("snd", 'A', ack_packet)
			
			fin_packet = receiver.stp_FIN(seq_num, ack_num)
			receiver.send_data(fin_packet,sender_addr)
			receiver.update_log("snd", 'F', fin_packet)

			# and then wait for feedback(ACK)
			ack_packet,sender_addr = receiver.recv_data()
			total_seg +=1
			receiver.update_log("rcv", 'A', ack_packet)
			length_data = ack_packet.seq_num - 2
			# receive sender ack, close.
			print('end')
			if ack_packet.ack == True:
				receiver.close_socket()
				break

	dup_ack = count_dup(l)

	print('STP CLOSE')

	line = "========================================\n"
	file = open('Sender_log.txt','a+')
	data = "Amount of Data Received = {} bytes\n".format(length_data)
	total_seg = "Total segments received = {}\n".format(total_seg)
	Data_seg = "Data segments received = {}\n".format(num_segment)
	error_Data = "Data Segments with bit errors = {}\n".format(num_error)
	dup_seg = "Duplicate data segments received  = {}\n".format(dup_ack)
	dup_ack_sent = "Duplicate Acks sent = {}\n".format(dup_ack_sent)

	file = open('Receiver_log.txt','a+')
	final_str = "\n"+line + data + total_seg +Data_seg+ error_Data + dup_seg + dup_ack_sent +line
	file.write(final_str)
	file.close()

	file = open(file_r,'ab+')
	file.write(total_data)
	file.close()
	'''
	#定义要生成的pdf的名称
	c=canvas.Canvas(file)
	#调用函数进行绘画，并将canvas对象作为参数传递
	generate_pdf(c,total_data.decode())
	#showPage函数：保存当前页的canvas
	c.showPage()
	#save函数：保存文件并关闭canvas
	c.save()
	'''

			

