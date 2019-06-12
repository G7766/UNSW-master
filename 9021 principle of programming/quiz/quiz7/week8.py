class Node:
    def __init__(self,value):
        self.value=value
        self.next= None
class Linkedlist:
    
    def __init__(self, L=None , key= lambda x:x):
        self.key=key
        if not L:
            self.head=None
            #self.length=0
        else:
            self.head=Node(L[0])
            node=self.head
            #self.length=1
            #go through each element in waht remains of the sequence
            for e in L[1:]:
                #make a new node out of the element we process..
                new_node=Node(e)
                #..and link it to what is currently the lastnode
                node.next=new_node
                #now the newly created and linked node become the last node
                # in the linked list under construction
                node=new_node
                #self.length +=1
        #return self.length
    
    def __len__(self):
        if not self.head:
            return 0
        length = 1
        node = self.head.next
        while node:
            length += 1
            node=node.next
        return length
    
    def print_list(self,seperator=','):
        if self.head:
            #collect all nodes by
            #first getting the first node...
            nodes=[str(self.head.value)]
            node=self.head.next           
        #and then, starting the node from the following node
        #and moving to 
        while node:
            nodes.append(str(node.value))
            node=node.next
        print(seperator.join(nodes))
    
    def extend(self,LL):
        if not self.head:
            self.head=LL.head
            return     
        node=self.head
        #go all the way to the end of my linked list
        while node.next:
            node=node.next
        #connect last node to LL's head
        node.next=LL.head
        
    def is_sorted(self):
        if len(self)<2:
            return True
        node=self.head
        # for as long as the current node has a following nodes
        while node.next:
            #if following node is strictly smaller
            if self.key(node.next.value) < self.key(node.value):
                return False
            node=node.next
        return True
    
    def delete_element(self,to_delete):
        if not self.head:
            return
        if self.head.value == to_delete:
            self.head=self.head.next
            return
        node=self.head
        #for as long as current node has following node and taht foloowing node
        #does not store the value to delete, then keep moving
        while node and node.next.value != to_delete:
            node=node.next
        
        # if next value has 
        if node.next:
            node.next=node.next.next
            
    def reverse(self):
        if len(self)<2:
            return
        R=self.head
        node=self.head.next
        self.head.next= None
        while node.next:
            node_next=node.next
            node.next=R
            R=node
            node=next_node
        node.next =R
        self.head=node

    def recursive_reserve(self):
    if len(self)<2:
    	return
    node=self.head
    while  node.next.next:
    	node=node.next
    	new_head=node.next
    	
            
        
            
            
n1=Node(3)
print(n1)
print(n1.value)
print(n1.next)
n2=Node('B')
print(n2.next)
print(n2.value)
n1.next=n2
print(n1.next.value)
n3=Node(3.14)
n2.next=n3
print(n2.next)
print(n1.next.next.value)

LL=Linkedlist([3,'J',3.14,11])
print(LL.head.value)
print(LL.head.next.next.value)
print(LL.head.next.next.next.value)
#print(LL.head.next.next.next.next.value)  None
print(len(LL))
LL_1=Linkedlist([3,'J',3.14,11])
LL_2=Linkedlist([3,1,45])
LL_1.extend(LL_2)
LL_1.print_list()
print('-------------')
LL_1=Linkedlist([3,5,7,7,11])
print(LL_1.is_sorted())
LL_1=Linkedlist([3,5,7,7,6,11])
print(LL_1.is_sorted())
LL_1=Linkedlist([1,-1,2,-2,4,-4],key=abs)
print(LL_1.is_sorted())
LL_1=Linkedlist([1,2,3,4,5])