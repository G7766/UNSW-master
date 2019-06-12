# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
    	#---
    	re_list=LinkedList()  
    	node = self.head
    	while node:
    		re_list.insert_sorted_value(node.value)
    		node=node.next_node
    	#相当于re_list=LinkedList([5, 33, 38, 49, 51, 53, 61, 62, 65, 97])
    	#re_list.print()
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
    					#print('a:',node.value,end=' ')
    					#print('len(arrange):',len(arrange))
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
        # Replace pass above with your code

    
    
    