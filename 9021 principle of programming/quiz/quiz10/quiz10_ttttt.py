import sys
from random import randint, seed
from binary_tree_adt import *
from math import log



class PriorityQueue(BinaryTree):
    def __init__(self):
        super().__init__()
        self.size=0
        self.pq_list=[None]*11

    def _bubble_up(self,position):
        if position==1:
            return
        if self.pq_list[position]>=self.pq_list[position//2]:
            return
        # position//2  is parent position
        if self.pq_list[position]<self.pq_list[position//2]:
            self.pq_list[position] , self.pq_list[position//2] =  self.pq_list[position//2] , self.pq_list[position]
            self._bubble_up(position//2)
    def insert(self, value):
        if value is None:
            return
        if value is not None:
            self.size +=1
            self.pq_list[self.size]=value
            self._bubble_up(self.size)
            q=0
            for z in range(len(self.pq_list)):
                if z>=1 and self.pq_list[z]!=None:
                    q +=1
            self.q=q
            #print(self.q)
            c=1
            #print(self.pq_list[1])
            self.list_create_tree(self,self.pq_list[c],self.pq_list,c)
            #level是层数
    
    def list_create_tree(self,root,value,list,c):
        if c <= self.q:
            #print('c:',c)
            root.value=value
            root.left_node=BinaryTree()
            root.right_node=BinaryTree()
            try:
                if list[2*c]!=None:
                    #print('2*c:',2*c)
                    root.left_node=BinaryTree(list[2*c])
                    self.list_create_tree(root.left_node,list[2*c],list,2*c)
                if list[2*c+1]!=None:
                    #print('2*c+1:',2*c+1)
                    root.right_node=BinaryTree(list[2*c+1])
                    self.list_create_tree(root.right_node,list[2*c+1],list,2*c+1)
            except:
                pass
                #print('error!')
        return











arg_for_seed=0
nb_of_nodes=4
seed(arg_for_seed)
pq = PriorityQueue()
for _ in range(nb_of_nodes - 1):
    pq.insert(randint(0, nb_of_nodes))
    pq.print_binary_tree()
    print()
pq.insert(randint(0, nb_of_nodes))
pq.print_binary_tree()