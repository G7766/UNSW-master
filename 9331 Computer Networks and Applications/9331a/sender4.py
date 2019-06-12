from socket import *
from random import *
import random
import time
import sys
import pickle
import threading

class STP_Packet:
	def __init__(self,data,seq_num,ack_num,ack = False, syn = False, fin = False,checksum = None):
		self.data = data
		self.seq_num = seq_num
		self.ack_num = ack_num
		self.ack = ack
		self.syn = syn
		self.fin = fin
		self.checksum = checksum

def delay(packet,time,sender):
   if time.time() - time >= sender.maxDelay:
   	sender.send_data(packet)
   	packet.ack_num = 1
   	sender.update_log('snd','D',packet)
   	ack_packet = sender.recv_data()
   	ack_packet.seq_num = 1
   	sender.update_log("rcv", 'A', ack_packet)
   	return 1


class Sender:
	# create sender side data
	def __init__(self, _host_ip, _port, file, MWS, MSS, gamma,pdrop, duplicated,
		pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed):
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
		self.pDelay = float(pDelay)
		self.maxDelay = float(maxDelay)/1000
		random.seed(int(seed))
		self.total_packet_num = 0
		#self.random = random.random()

	# create UDP socket
	sender_socket = socket(AF_INET,SOCK_DGRAM)
	#sender_socket.settimeout(2)

	#read file to data
	def read_data(self):
		with open(self.file,'rb') as f:
			data = f.read()
		return data

	def get_total_packet_num(self,data):
		size = len(data)
		num_packet = size//self.MSS
		if (size%self.MSS!=0):
			num_packet = num_packet + 1
		self.total_packet_num = num_packet
		return num_packet

	def split_data(self,data,data_progress):
		size = len(data)
		new = data_progress + self.MSS 
		if new < size:
			payload = data[data_progress:new]
		else:
			payload = data[data_progress:size]

		return payload
	# send segment
	def send_data(self,packet):
		self.sender_socket.sendto(pickle.dumps(packet),self.addr)

	# receive data from server
	def recv_data(self):
		try:
			data,addr = self.sender_socket.recvfrom(2048)
			recv_packet = pickle.loads(data)
			return recv_packet
		except:
			return False


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
		sender.update_log("snd", 'RXT',packet)
		#print(':::: R_seq: {}'.format(packet.seq_num))

	# Record time
	def start_timer(self):
		self.start_time = time.time() * 1000
		return self.start_time
	
	def current_time(self):
		self.current_time = time.time() * 1000
		return self.current_time

	def previous_time(self):
		self.previous_time = time.time() * 1000
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

	# PLD module:

	def PLD_pdrop(self):
		r = random.random()
		#print(r)
		if r > self.pdrop:
			return False
		return True
	def PLD_pDuplicate(self):
		r = random.random()
		#print('r_Duplicate:',r)
		if r > self.duplicated:
			return False
		return True
	def PLD_pCorrupt(self):
		r = random.random()
		#print('r_Corrupt:',r)
		if r > self.pCorrupt:
			return False
		return True
	def PLD_pOrder(self):
		r = random.random()
		if r > self.pOrder:
			return False
		return True
	def PLD_pDelay(self):
		r = random.random()
		if r > self.pDelay:
			return False
		return True
	def PLD_check(self):
		if self.PLD_pdrop()==False:
			if self.PLD_pDuplicate()==False:
				if self.PLD_pCorrupt()==False:
					if self.PLD_pOrder()==False:
						if self.PLD_pDelay()==False:
							return 0
						else:
							print('packet delay!')
							return 5
					else:
						print('packet reorder!')
						return 4
				else:
					print('packet corrupt!')
					return 3
			else:
				print('packet pDuplicate!')
				return 2
		else:
			print('packet drop!')
			return 1


if __name__ =='__main__':
	# give value and ready to start
	receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop,duplicated,pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed= sys.argv[1:]
	print('Host: {}\nPort: {}\nFile: {}\nMWS: {}\nMSS: {}\ngamma: {}\npdrop: {}\nduplicated: {}\npCorrupt: {}\npOrder: {}\nmaxOrder: {}\npDelay: {}\nmaxDelay: {}\nseed: {}\n'
		.format(receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop, duplicated,
		pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed))
	seq_num = 0
	ack_num = 0
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

	num_transmitted=0
	PLD_seg = 0
	num_retransmitted=0
	num_dropped = 0
	num_delay = 0
	num_corrupt = 0
	num_reorder = 0
	num_duplicate = 0
	timeout_retransmitted = 0
	num_fast_retrans = 0
	num_dup_ack = 0
	num_trans_data = 0

	num_notyet_acked = 0 

	# Start Sender class
	print('Sender Start:')
	sender = Sender(receiver_host_ip, receiver_port, file, MWS, MSS, gamma,pdrop,duplicated,pCorrupt,pOrder,maxOrder,pDelay,maxDelay,seed)
	#a=int(seed)
	#print(a)
	#random.seed(a)
	#random = random.random()
	#sender.random = random
	#print(sender.random )
	stp_data = sender.read_data()
	#with open("test1.txt",'r') as f:
	#	stp_data = f.read()

	window_size = sender.MWS//sender.MSS
	print('Window size:',window_size)
	window = []


	# count packet number and unacked packets
	curr_packet_number = 0
	packet_info = {}

	# info of the data already send
	data_progress = 0
	length_data = len(stp_data)
	print('Data length: {}'.format(length_data))

	num_acked = 0
	#print('Total paket number: ', sender.get_total_packet_num(stp_data))
	num_segment = sender.get_total_packet_num(stp_data)
	#TimeoutInterval
	#EstimatedRTT = 500 milliseconds 
	#DevRTT = 250 milliseconds
	#TimeoutInterval = EstimatedRTT + gamma * DevRTT =0.5+1 =1.5 s
	timeoutInterval = 0.5 + sender.gamma * 0.25
	#timeoutInterval = 0.39
	re_ordering_list = []
	num_reording = 0

	sendbase = 0
	number_loop = 0
	timer = 0
	# pdrop is random number

	delay_flag = 0
	delay_count = 0
	delay_packet = []
	time_list = []
	# bytearray
	# dump
	while True:
		# use for check PLD
		flag = 0
		print('***** number of loop: {} *****'.format(number_loop))
		number_loop = number_loop + 1

		

		# if the connection is closed, need to create connection and send SYN
		if stp_closed_state == True:
			#Sender first send the syn to connect
			syn_packet = sender.stp_SYN(seq_num,ack_num)
			sender.send_data(syn_packet)
			num_transmitted = num_transmitted + 1
			sender.update_log("snd", 'S',syn_packet)
			stp_closed_state = False
			stp_syn_sent = True
			print('***** State: Connected *****')


		# if SYN has been sent:
		if stp_syn_sent == True:
			# get the ack
			syn_ack_packet = sender.recv_data()
			if syn_ack_packet.ack == True and syn_ack_packet.syn == True:
				# syn and ack are all True, log update
				ack_num = syn_ack_packet.seq_num + 1
				sender.update_log("rcv", 'SA',syn_ack_packet)

				#send ACK
				seq_num = seq_num + 1
				ack_packet = sender.stp_ACK(seq_num,ack_num)
				sender.send_data(ack_packet)
				num_trans_data = num_trans_data + 1
				num_transmitted = num_transmitted+1
				sender.update_log("snd", 'A',ack_packet)
				# 3-way-handshake complete
				state_established = True
				stp_syn_sent = False
				stp_ack_sent = True
				print('3-way-handshake complete')


		while state_established == True:
			flag = 0  
			if len(window) != window_size:
				'''
				if delay_packet!=[] and time.time()>=time_list[0]:
					#print(time.time())
					#if time.time()>=nexttime:
					print('!!~~~')
					delay_packet.seq_num = seq_num
					sender.send_data(delay_packet)
					delay_packet.ack_num = 1
					sender.update_log("dely", 'D',delay_packet)
					#if timeoutInterval < time.time()- timer:
					#	sender.retransmit(packet)
					ack_packet = sender.recv_data()
					ack_packet.seq_num = 1 
					sender.update_log("rcv", 'A',ack_packet)
					#seq_num =  seq_num + len(reOrding_packet.data)
					print('dely success!')
					seq_num =  seq_num + len(delay_packet.data)
					#ack_num = ack_num + len(ack_packet.data)
					delay_packet.pop(0)
					time_list.pop(0)
					continue
				'''

				if re_ordering_list!= []:
					num_reording +=1
					if num_reording == sender.maxOrder +1:
						#flag = 'Reording finish!':
						reOrding_packet = re_ordering_list[0]
						reOrding_packet.seq_num = seq_num
						re_ordering_list = []
						sender.send_data(reOrding_packet)
						num_transmitted = num_transmitted + 1
						reOrding_packet.ack_num = 1
						sender.update_log("rord", 'D',reOrding_packet)
						#if timeoutInterval < time.time()- timer:
						#	sender.retransmit(packet)
						ack_packet = sender.recv_data()
						ack_packet.seq_num = 1 
						sender.update_log("rcv", 'A',ack_packet)
						#seq_num =  seq_num + len(reOrding_packet.data)
						print('reOrding success!')
						seq_num =  seq_num + len(reOrding_packet.data)
						#ack_num = ack_num + len(ack_packet.data)
						continue


				#create packet
				payload = sender.split_data(stp_data,data_progress)
				checksum = payload
				packet = STP_Packet(payload,seq_num,ack_num,ack=False,syn=False,fin=False,checksum=checksum)
				if timer ==0:
					timer = sender.start_timer()
				#sender.PLD(packet)
				# check PLD
				check = sender.PLD_check()
				if check == 0 :
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					sender.update_log('snd','D',packet)
					print('packet send successfully.')
					seq_num = seq_num + len(payload)
					num_notyet_acked += 1
					window.append(seq_num)
					PLD_seg +=1
				elif check == 1:
					print('test')
					sender.update_log("drop", 'D', packet)
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					sender.update_log("snd", 'RXT',packet)
					seq_num = seq_num + len(payload)
					num_notyet_acked += 1
					window.append(seq_num)
					PLD_seg +=1
					num_dropped +=1
					num_fast_retrans = num_fast_retrans+1
				elif check == 2:
					flag = 2
					# 1
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					sender.update_log('snd','D',packet)
					#seq_num = seq_num + len(payload)
					print(packet.seq_num,'===',packet.ack_num )

					ack_packet = sender.recv_data()
					ack_packet.seq_num = 1
					sender.update_log("rcv", 'A', ack_packet)
					# 2
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					sender.update_log('dup','D',packet)
					
					seq_num = seq_num + len(payload)
					num_notyet_acked += 1
					window.append(seq_num)
					PLD_seg +=1
					num_duplicate +=1
					num_dup_ack +=1
				elif check == 3:
					#flag = 3
					payload = sender.split_data(stp_data,data_progress)
					checksum = payload
					z = bytearray(payload)
					z[0] = 1
					new_load = bytes(z)
					packet = STP_Packet(new_load,seq_num,ack_num,ack=False,syn=False,fin=False,checksum=checksum)
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					sender.update_log('corr','D',packet)
					#ack_packet = sender.recv_data()
					#ack_packet.seq_num = 1
					packet.ack_num = packet.seq_num
					packet.seq_num = 1
					packet.data = ''
					sender.update_log("rcv", 'A', packet)

					#time.sleep(0.1)
					payload = sender.split_data(stp_data,data_progress)
					packet = STP_Packet(payload,seq_num,ack_num,ack=False,syn=False,fin=False,checksum=payload)
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					seq_num = seq_num + len(payload)
					sender.update_log('snd','D',packet)
					window.append(seq_num)
					print(packet.seq_num, '!!!!!', packet.ack_num)
					PLD_seg +=1
					num_corrupt +=1
				elif check == 4:
					if re_ordering_list!=[] or sender.maxOrder + num_trans_data >= num_segment:
						sender.send_data(packet)
						num_transmitted = num_transmitted + 1
						num_trans_data +=1
						packet.ack_num = 1
						sender.update_log('snd','D',packet)
						print('packet send successfully.')
						seq_num = seq_num + len(payload)
						num_notyet_acked += 1
						window.append(seq_num)
					else:
						re_ordering_list.append(packet)
						print('<< Packet reOrding >>')
						data_progress = data_progress + len(payload)
						num_reorder = num_reorder + 1
						PLD_seg +=1
						continue
				elif check == 5:
					nowtime = time.time()
					nexttime = nowtime + sender.maxDelay
					while True:
						if time.time() == nexttime:
							break
					sender.send_data(packet)
					num_transmitted = num_transmitted + 1
					num_trans_data +=1
					packet.ack_num = 1
					sender.update_log('dely','D',packet)
					print('packet send successfully.')
					seq_num = seq_num + len(payload)
					num_notyet_acked += 1
					window.append(seq_num)
					PLD_seg +=1
					num_delay +=1
					'''
					nowtime = time.time()
					nexttime = nowtime + sender.maxDelay
					print('now:',nowtime)
					print('next:',nexttime)
					delay_packet.append(packet)
					time_list.append(nexttime)
					data_progress = data_progress + len(payload)
					delay_flag = 1
					continue
					'''

			if timeoutInterval < time.time()- timer:
					sender.retransmit(packet)
					timeout_retransmitted +=1
			if flag ==0:
				# if timeout retransmit!
				if timeoutInterval < time.time()- timer:
					sender.retransmit(packet)	
				
				data_progress += len(payload)
				ack_packet = sender.recv_data()
				sender.update_log("rcv", 'A', ack_packet)
				ack_num = ack_num + len(ack_packet.data)
				print('?????')
			elif flag ==2:
				if timeoutInterval < time.time()- timer:
					sender.retransmit(packet)	
				
				data_progress += len(payload)
				ack_num = ack_num + len(ack_packet.data)

			print(window)
			y= ack_packet.ack_num
			if y > sendbase:
				sendbase = y
				window.pop(0)
				num_notyet_acked -=1
				if num_notyet_acked!=0:
					timer = sender.start_timer()

			if data_progress == length_data :
				fin_packet = sender.stp_FIN(seq_num,ack_num)
				sender.send_data(fin_packet)
				num_transmitted = num_transmitted + 1
				sender.update_log('snd','F',fin_packet)
				state_end = True
				state_established = False
				break
		
		if state_end == True:
			#time.sleep(1)
			print('End the connection:')
			ack_packet = sender.recv_data()
			sender.update_log("rcv", 'A',ack_packet)
			if ack_packet.ack == True:
				fin_packet = sender.recv_data()
				#if fin_packet.ack == True:
				sender.update_log("rcv", 'F',fin_packet)
				if fin_packet.fin == True:
					ack_num = ack_num + 1
					seq_num = fin_packet.ack_num
					ack_packet = sender.stp_ACK(seq_num,ack_num)
					sender.send_data(ack_packet)
					num_transmitted = num_transmitted + 1
					sender.update_log("snd", 'A',ack_packet)
					print("Waiting 5 seconds")
					time.sleep(1)
					break

	sender.close_socket()
	print('STP CLOSE')
	line = "========================================\n"
	file = open('Sender_log.txt','a+')
	data = "Data Transferred = {} bytes\n".format(length_data)
	seg_sent = "Segments transmitted = {}\n".format(num_transmitted)
	PLD_handled = "Number of Segments handled by PLD  = {}\n".format(PLD_seg)
	pkt_dropped = "Number of Segments Dropped = {}\n".format(num_dropped)
	pkt_corrupt = "Number of Segments Corrupted= {}\n".format(num_corrupt)
	pkt_rorr = "Number of Segments Re-ordered= {}\n".format(num_reorder)
	pkt_duplicate = "Number of Segments Duplicated = {}\n".format(num_duplicate)
	pkt_delayed = "Number of Segments Delayed = {}\n".format(num_delay)
	seg_retrans = "Number of Retransmissions due to timeout = {}\n".format(timeout_retransmitted)
	fast_seg_retrans = "Number of Fast Retransmissions = {}\n".format(num_fast_retrans)
	num_dup_seg_ack = "Number of Duplicate Acknowledgements received  = {}\n".format(num_dup_ack)
	final_str = "\n"+line + data + seg_sent +PLD_handled+ pkt_dropped + pkt_corrupt + pkt_rorr + pkt_duplicate + pkt_delayed+seg_retrans+fast_seg_retrans+num_dup_seg_ack+line
	file.write(final_str)
	file.close()























