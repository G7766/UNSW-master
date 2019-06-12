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
import threading


# (14) arguments:  
# 6 arguments
# receiver_host_ip, receiver_port, file.pdf, 
# MWS, MSS, gamma, 
# 8 arguments are used exclusively by the PLD module:
# pDrop, pDuplicate, pCorrupt, maxOrder, pDelay, maxDelay
# seed

class Send_Thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release()















