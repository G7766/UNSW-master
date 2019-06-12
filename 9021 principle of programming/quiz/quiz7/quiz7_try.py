import sys
from random import seed, randrange
from copy import deepcopy

class Node:
    def __init__(self, value = None):
        self.value = value
        self.next_node = None
class LinkedList:
    def __init__(self, L = None, key = lambda x: x):

        self.key = key
        if L is None:
            self.head = None
            return
        # If L is not subscriptable, then will generate an exception that reads:
        # TypeError: 'type_of_L' object is not subscriptable
        if not len(L[: 1]):
            self.head = None
            return
        node = Node(L[0])
        self.head = node
        for e in L[1: ]:
            node.next_node = Node(e)
            node = node.next_node

    def print(self, separator = ', '):
        if not self.head:
            return
        nodes = []
        node = self.head
        while node:
            nodes.append(str(node.value))
            node = node.next_node
        print(separator.join(nodes))

    def __len__(self):
        '''
        >>> len(LinkedList())
        0
        >>> len(LinkedList([0]))
        1
        >>> len(LinkedList((0, 1)))
        2
        '''
        length = 0
        node = self.head
        while node:
            length += 1
            node = node.next_node
        return length
    
    def apply_function(self, function):
        '''
        >>> L = LinkedList(range(3))
        >>> L.apply_function(lambda x: 2 * x)
        >>> L.print()
        0, 2, 4
        '''
        node = self.head
        while node:
            node.value = function(node.value)
            node = node.next_node

    def is_sorted(self):
        node = self.head
        while node and node.next_node:
            if self.key(node.value) > self.key(node.next_node.value):
                return False
            node = node.next_node
        return True

    def index_of_value(self, value):

        index = 0
        node = self.head
        while node:
            if node.value == value:
                return index
            index += 1
            node = node.next_node
        return -1
    def insert_sorted_value(self, value):

        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        if value <= self.key(self.head.value):
            new_node.next_node = self.head
            self.head = new_node
            return
        node = self.head
        while node.next_node and value > self.key(node.next_node.value):
            node = node.next_node
        new_node.next_node = node.next_node
        node.next_node = new_node
    def prepend(self, value):
        if not self.head:
            self.head = Node(value)
            return
        head = self.head
        self.head = Node(value)
        self.head.next_node = head
            
    def append(self, value):

        if not self.head:
            self.head = Node(value)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = Node(value)
        ''' 
    def rearrange1(self):
    	re_list=LinkedList()  
    	node = self.head
    	while node:
    		re_list.insert_sorted_value(node.value)
    		node=node.next_node
    	#相当于re_list=LinkedList([5, 33, 38, 49, 51, 53, 61, 62, 65, 97])
    	re_list.print()
    	self.re_list=re_list
    	#print(re_list.head.value)
    	min_element=re_list.head.value
    	self.min_element=min_element
    	print(min_element)
    	min_element_index=LL.index_of_value(min_element)
    	self.min_element_index=min_element_index
    	print(self.min_element_index)
    	return
    	#print('???:',len(re_list))
    	#self.q=len(re_list)
    	'''

    def rearrange(self):
    	#---
    	re_list=LinkedList()  
    	node = self.head
    	while node:
    		re_list.insert_sorted_value(node.value)
    		node=node.next_node
    	#相当于re_list=LinkedList([5, 33, 38, 49, 51, 53, 61, 62, 65, 97])
    	re_list.print()
    	self.re_list=re_list
    	#print(re_list.head.value)
    	min_element=re_list.head.value
    	self.min_element=min_element
    	#print(min_element)
    	#min_element_index=LL.index_of_value(min_element)
    	#self.min_element_index=min_element_index
    	#print(self.min_element_index)
    	#------------
    	arrange=LinkedList()
    	node = self.head
    	next_element=self.min_element
    	while node:
    		if node.next_node.value==next_element:      #最开始next_element=最小数
    			#arrange.append(node.next_node.value)
    			#arrange.append(node.value)
    			while len(arrange)!=len(self.re_list):
    				if node:
    					print('a:',node.value,end=' ')
    					print('len(arrange):',len(arrange))
    					arrange.append(node.next_node.value)
    					arrange.append(node.value)
    					#arrange.prepend(node.next_node.value)
    					if node.next_node:
    						node=node.next_node
    						#print('b:',node)
    						if node.next_node:
    							node=node.next_node
    						else:
    							node=self.head
    			break
    		else:
    			node=node.next_node
    		#if len(arrange())>=2:

    		#if next_element==self.min_element:
    			#break
    		#if len(arrange())==len(re_list()):
    			#break
    	arrange.print()
        return arrange




'''
def __init__(self, L = None, key = lambda x: x):

        self.key = key
        if L is None:
            self.head = None
            return
        # If L is not subscriptable, then will generate an exception that reads:
        # TypeError: 'type_of_L' object is not subscriptable
        if not len(L[: 1]):
            self.head = None
            return
        node = Node(L[0])
        self.head = node
        for e in L[1: ]:
            node.next_node = Node(e)
            node = node.next_node
'''




arg_for_seed=0
length=3
length=(abs(int(length)) + 2) * 2
seed(arg_for_seed)
L = [randrange(100) for _ in range(length)]
#l=[1,2,3]
#a=l.index(2)
#print(a)
#print(L)
#print('L[:1]',L[:1])
#p=L.index(min(L))
#print(p)




LL=LinkedList(L)

LL.print()
#print('head:',LL.head)
#print('head:',LL.head.value)
#print('head:',LL.head.next_node)
#print('head:',LL.head.next_node.value)
#print(LL.__len__())
#L_sort=LinkedList(L).is_sorted()
#print(L_sort)
#print(LL.index_of_value(62))
'''
min_element=100
for i in L:
	if i<=min_element:
		min_element=i
print(min_element)
'''
#LL.rearrange()
print('----')
#LL.rearrange1()
#print(len(LL))
#LL.rearrange1()
LL.rearrange()
LL.print()





