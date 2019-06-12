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
	#sender_socket.settimeout(1)

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
		sender.update_log("snd", 'RXT',packet)
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

	# PLD module:

	def PLD_pdrop(self):
		r = random.random()
		if r > self.pdrop:
			return False
		return True
	def PLD_pDuplicate(self):
		r = random.random()
		print('r_Duplicate:',r)
		if r > self.duplicated:
			return False
		return True
	def PLD_pCorrupt(self):
		r = random.random()
		print('r_Corrupt:',r)
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


	# count packet number and unacked packets
	curr_packet_number = 0
	packet_info = {}

	# info of the data already send
	data_progress = 0
	length_data = len(stp_data)
	print('Data length: {}'.format(length_data))

	num_acked = 0
	print('Total paket number: ', sender.get_total_packet_num(stp_data))
	num_segment = sender.get_total_packet_num(stp_data)
	#TimeoutInterval
	#EstimatedRTT = 500 milliseconds 
	#DevRTT = 250 milliseconds
	#TimeoutInterval = EstimatedRTT + gamma * DevRTT =0.5+1 =1.5 s
	timeoutInterval = 0.5 + sender.gamma * 0.25
	#timeoutInterval = 0.39
	
	sendbase = 0
	# pdrop is random number

	#print('!!!!!!!!!!!!!!!!!random:',sender.random)
	print('Loop:')
	number_loop=0
	num_reording = 0
	re_ordering_list = []
	while True:
		# use for check PLD
		flag = 0
		print('***** number of loop: {} *****'.format(number_loop))
		number_loop = number_loop+1

		

		# if the connection is closed, need to create connection and send SYN
		if stp_closed_state == True:
			print('***** State: closed. Ready to send SYN *****')
			#Sender first send the syn to connect
			syn_packet = sender.stp_SYN(seq_num,ack_num)
			sender.send_data(syn_packet)
			num_transmitted = num_transmitted+1
			sender.update_log("snd", 'S',syn_packet)
			stp_closed_state = False
			stp_syn_sent = True
			print('***** State: Connected *****')


		# if SYN has been sent:
		if stp_syn_sent == True:
			print('***** State: SYN has been sent *****')
			# get the ack
			syn_ack_packet = sender.recv_data()
			print('!!!!')
			if syn_ack_packet.ack == True and syn_ack_packet.syn == True:
				# syn and ack are all True, log update
				ack_num = syn_ack_packet.seq_num + 1
				sender.update_log("rcv", 'SA',syn_ack_packet)

				#send ACK
				seq_num = seq_num + 1
				ack_packet = sender.stp_ACK(seq_num,ack_num)
				sender.send_data(ack_packet)
				num_transmitted = num_transmitted+1
				sender.update_log("snd", 'A',ack_packet)
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

			# the number of loop since reOrding happen
		
			if re_ordering_list!= []:
				num_reording +=1
				if num_reording == sender.maxOrder +1:
					#flag = 'Reording finish!':
					reOrding_packet = re_ordering_list[0]
					reOrding_packet.seq_num = seq_num
					re_ordering_list = []
					sender.send_data(reOrding_packet)
					sender.update_log("rord", 'D',reOrding_packet)
					num_transmitted = num_transmitted + 1
					num_reording = 0
					ack_packet = sender.recv_data()
					sender.update_log("rcv", 'A',ack_packet)
					seq_num =  seq_num + len(reOrding_packet.data)
					print('reOrding success!')
					num_acked = num_acked+1
					PLD_seg = PLD_seg + 1
					continue


			# create packet
			payload = sender.split_data(stp_data,data_progress)
			print('!!!!!!!!!!!!!!!!!:',len(payload))
			packet = STP_Packet(payload,seq_num,ack_num,ack=False,syn=False,fin=False)

			#print(payload)
			#break

			curr_time = time.clock() * 1000
			diff_time = curr_time - previous_time
			print("Current time: {}".format(curr_time))
			print("Pevious time: {}".format(previous_time))
			print("Time diff: {}".format(diff_time))
			print("Timeout: {}".format(timeoutInterval))
			# check the previous packet has acked or not, 
			# if exists and over timeout time 
			# then retransmit:  (use not_acked_num)
			if previous_packet != None and diff_time > timeoutInterval:
				print('Retransmitting!')
				sender.retransmit(previous_packet);
				num_retransmitted += 1
				num_acked = num_acked + 1
				previous_packet = None
				timeout_retransmitted = timeout_retransmitted +1
				continue

			# packet not for connection
			#check PLD:
			# 1st check pdrop
			pld_pdrop_check = sender.PLD_pdrop()
			# not drop
			if pld_pdrop_check == False:
				# 2nd check duplicated
				pld_duplicated_check = sender.PLD_pDuplicate()
				if pld_duplicated_check == False:
					# 3rd check pCorrupt
					pld_pcorrupt_check = sender.PLD_pCorrupt()
					if pld_pcorrupt_check == False:
						# 4th check pOrder
						pld_preorder_check = sender.PLD_pOrder()
						if pld_preorder_check == False:
							# 5th check delay:
							pld_pdealy_check = sender.PLD_pDelay()
							if pld_pdealy_check == False:
								# get the oldest unacknowledged segment
								# if timer currently not running :start running
								previous_time = time.clock() * 1000
								# pass segment to ip
								sender.send_data(packet)
								print(len(payload))
								previous_packet = packet
								print('<< Packet send suceessfully >>')
								#print(':::: seq: {}'.format(packet.seq_num))
								#not_acked_num = not_acked_num + 1
								#nextSeqNum = nextSeqNum + length(data)
								seq_num =  seq_num + len(payload)
								packet.ack_num = 1
								sender.update_log('snd','D',packet)
								num_transmitted = num_transmitted + 1
								PLD_seg = PLD_seg + 1
							else:
								#pass
								# 延时发送
								# get the oldest unacknowledged segment
								# if timer currently not running :start running
								if sender.start_time == 0:
									sender.start_timer()
									print('Start time: {}\n'.format(sender.start_time))
								print('Packet Delay!')
								now_time = time.time()
								next_time = now_time + sender.maxDelay
								print('now_time: ',now_time)
								print('next_time: ',next_time)
								num_delay = num_delay+1
								#Delay_packet = packet
								#sender.send_data(packet)
								#data_progress = data_progress + len(payload)
								#Delay_packet.seq_num = seq_num
								while True:
									if time.time() >= next_time:
										break
								previous_time = time.clock() * 1000
								sender.send_data(packet)
								packet.ack_num = 1
								sender.update_log("dely", 'D',packet)
								seq_num =  seq_num + len(packet.data)
								num_transmitted = num_transmitted + 1
								num_acked = num_acked +1
								PLD_seg = PLD_seg + 1
								

						else:
							#save the current STP segment and wait for forwarding of maxOrder
							# if already exist in re_ordering_list, send to receiver directly
							if re_ordering_list!=[]:
								#flag = 0
								if sender.start_time == 0:
									sender.start_timer()
									print('Start time: {}\n'.format(sender.start_time))
								# pass segment to ip
								sender.send_data(packet)
								print('<< Packet send suceessfully >>')
								#not_acked_num = not_acked_num + 1
								#nextSeqNum = nextSeqNum + length(data)
								seq_num =  seq_num + len(payload)
								packet.ack_num = 1
								sender.update_log('snd','D',packet)
								num_transmitted = num_transmitted + 1
								PLD_seg = PLD_seg + 1
								num_reorder = num_reorder +1
							# else:
							else:
								re_ordering_list.append(packet)
								print('<< Packet reOrding >>')
								data_progress = data_progress + len(payload)
								num_reorder = num_reorder + 1
								#seq_num =  seq_num + len(payload)
								continue
					else:
						#flag = 3
						#print('!!!!!',len(packet.data))
						print('Packet pCorrupt!')
						original_packet = packet
						#print('?????',len(original_packet.data))
						packet.data = str(packet.data)
						#checksum
						packet.checksum = packet.data
						if sender.start_time == 0:
							sender.start_timer()
							#print('Start time: {}\n'.format(sender.start_time))
						# introduce one str error
						#packet.data = str(packet.data)
						l = list(packet.data)
						if l[2] == '1':
							l[2] = '0'
						else:
							l[2] = '1'
						packet.data = ''.join(l)
						#packet.data = int(packet.data)
						sender.send_data(packet)
						#previous_time = time.clock() * 1000
						payload = sender.split_data(stp_data,data_progress)
						#print('!!!!!!!!!!!!!!!!!:',len(payload))
						packet = STP_Packet(payload,seq_num,ack_num,ack=False,syn=False,fin=False)
						sender.retransmit(packet)
						#print('~~~!!!!!',len(packet.data))
						#previous_packet = packet
						#not_acked_num = not_acked_num + 1
						#nextSeqNum = nextSeqNum + length(data)
						seq_num =  seq_num + len(payload)
						original_packet.ack_num = 1
						sender.update_log('corr','D',original_packet)
						num_transmitted = num_transmitted + 1
						num_fast_retrans = num_fast_retrans + 1
						num_corrupt = num_corrupt + 1
						PLD_seg = PLD_seg + 1
				else:
					#flag = 2
					if sender.start_time == 0:
						sender.start_timer()
					#print('Start time: {}\n'.format(sender.start_time))
					# 1 st wait for ack
					print('Packet pDuplicate!')
					sender.send_data(packet)
					print(packet.seq_num)
					print(packet.ack_num)
					packet.ack_num = 1
					sender.update_log('snd','D',packet)
					ack_packet = sender.recv_data()
					sender.update_log("rcv", 'A',ack_packet)
					num_transmitted = num_transmitted + 1
					print('pDuplicate 1 sent!')
					
					# 2nd duplicate packet
					previous_time = time.clock() * 1000
					sender.send_data(packet)
					previous_packet = packet
					packet.ack_num = 1
					sender.update_log('dup','D',packet)
					print(packet.seq_num)
					print(packet.ack_num)

					num_transmitted = num_transmitted + 1
					print('pDuplicate 2 sent!')
					seq_num =  seq_num + len(payload)
					num_duplicate = num_duplicate + 1
					PLD_seg = PLD_seg + 1
					num_dup_ack = num_dup_ack +1

			# drop:
			else:
				print('Packet Drop!')
				previous_time = time.clock() * 1000
				sender.update_log("drop", 'D', packet)
				# store drop packet and wait for retransmit
				#previous_packet.append(packet)
				sender.retransmit(packet)
				num_dropped = num_dropped + 1
				seq_num += len(payload)
				num_transmitted =num_transmitted + 1
				PLD_seg = PLD_seg + 1
				num_fast_retrans = num_fast_retrans + 1
			


			if curr_time == 0:
				curr_time = sender.current_time()

			data_progress += len(payload)
			# transfer successfully
			print('State: wait for ack')
			ack_packet = sender.recv_data()
			print('????')
			sender.update_log("rcv", 'A', ack_packet)
			ack_num = ack_num + len(ack_packet.data)

			print('num_acked: ',num_acked)
			# 四次挥手
			'''
			（1）客户端A发送一个FIN，用来关闭客户A到服务器B的数据传送（报文段4）。
			（2）服务器B收到这个FIN，它发回一个ACK，确认序号为收到的序号加1（报文段5）。和SYN一样，一个FIN将占用一个序号。
			（3）服务器B关闭与客户端A的连接，发送一个FIN给客户端A（报文段6）。
			（4）客户端A发回ACK报文确认，并将确认序号设置为收到序号加1（报文段7）
			'''
			# the data progress equal to len of data(entire file)
			# the file is trinsfered complete, close connection
			if data_progress == length_data :
				#ack_num = 1
				# client send fin to receiver to close
				fin_packet = sender.stp_FIN(seq_num,ack_num)
				sender.send_data(fin_packet)
				fin_packet.ack_num = 1
				num_transmitted = num_transmitted + 1
				sender.update_log('snd','F',fin_packet)
				state_end = True
				state_established = False
		
		# if state_end is ture:
		if state_end == True :
			print('End the connection:')
			# get ack packet from receiver
			time.sleep(1)
			ack_packet = sender.recv_data()
			if ack_packet.ack == True:
				fin_packet = sender.recv_data()
				if fin_packet.ack == True:
					sender.update_log("rcv", 'A',fin_packet)
				if fin_packet.fin == True:
					sender.update_log("rcv", 'F',fin_packet)

				while fin_packet.fin != True:
					fin_packet = sender.recv_data()
					if fin_packet.ack == True:
						sender.update_log("rcv", 'A',fin_packet)
					#fin_packet.fin == True:
				ack_num = ack_num + 1
				print('test4')
				# send ACK
				ack_packet = sender.stp_ACK(seq_num,ack_num)
				sender.send_data(ack_packet)
				num_transmitted = num_transmitted + 1
				sender.update_log("snd", 'A',ack_packet)
				print("Waiting 5 seconds")
				time.sleep(5)
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























