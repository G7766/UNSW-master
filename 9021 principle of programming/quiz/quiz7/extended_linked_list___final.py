# Written by **** for COMP9021

from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        re_list=LinkedList() 
        node = self.head
        #print('aaaa:',node.value)
        #print(node)
        while node:
            re_list.insert_sorted_value(node.value)
            node=node.next_node
            #re_list.print()
            self.re_list=re_list
        min_element=re_list.head.value
        #print('ccc',min_element)
        self.min_element=min_element
        arrange=LinkedList()
        node = self.head
        #print('bbbb',node.value)
        #print(node)
        next_element=self.min_element
        while node:
            if node.next_node.value==next_element:
                while len(arrange)!=len(self.re_list):
                    if node:
                        #print('a:',node.value,end=' ')
                        #print('len(arrange):',len(arrange))
                        arrange.append(node.next_node.value)
                        arrange.append(node.value)
                        if node.next_node:
                            node=node.next_node
                            if node.next_node:
                                node=node.next_node
                            else:
                                node=self.head
                                #print(node.value)
                                #print(node)
                break
            else:
                node=node.next_node
        #print('-------------')
        #arrange.print()
        node=self.head
        #print('???',node)
        #print(self.head.value)
        self.head.value=arrange.head.value
        q=arrange.head.next_node
        while node:
            #print('a:',node.value)
            node=node.next_node
            if q:
                node.value=q.value
                q=q.next_node
            else:
                break
        return
        # Replace pass above with your code

    
    
    