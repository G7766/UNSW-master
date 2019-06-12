
class BinaryTree:
    def __init__(self, value = None):
        self.value = value
        if self.value is not None:
            self.left_node = BinaryTree()
            self.right_node = BinaryTree()
        else:
            self.left_node = None
            self.right_node = None

    def height(self):

        if self.value is None:
            return 0
        return max(self.left_node._height(), self.right_node._height())

    def _height(self):
        if self.value is None:
            return 0
        return max(self.left_node._height(), self.right_node._height()) + 1

    def size(self):

        if self.value is None:
            return 0
        return 1 + self.left_node.size() + self.right_node.size()

    def occurs_in_tree(self, value):

        if self.value is None:
            return False
        if self.value == value:
            return True
        return self.left_node.occurs_in_tree(value) or self.right_node.occurs_in_tree(value)

    def occurs_in_bst(self, value):

        if self.value is None:
            return False
        if self.value == value:
            return True
        if value < self.value:
            return self.left_node.occurs_in_bst(value)
        return self.right_node.occurs_in_bst(value)

    def is_bst(self):
        if self.value is None:
            return True
        node = self.left_node
        if node.value is not None:
            while node.right_node.value is not None:
                node = node.right_node
            if self.value <= node.value:
                return False
        node = self.right_node
        if node.value is not None:
            while node.left_node.value is not None:
                node = node.left_node
            if self.value >= node.value:
                return False
        return self.left_node.is_bst() and self.right_node.is_bst()

    def insert_in_bst(self, value):

        if self.value is None:
            self.value = value
            self.left_node = BinaryTree()
            self.right_node = BinaryTree()
            return True
        if self.value == value:
            return False
        if value < self.value:
            return self.left_node.insert_in_bst(value)
        return self.right_node.insert_in_bst(value)


    def delete_in_bst(self, value):
        return self._delete_in_bst(value, self, '')

    def _delete_in_bst(self, value, parent, link):
        if self.value is None:
            return False
        if value < self.value:
            return self.left_node._delete_in_bst(value, self, 'L')
        if value > self.value:
            return self.right_node._delete_in_bst(value, self, 'R')
        if self.left_node.value is None:
            new_tree = self.right_node
        elif self.right_node.value is None:
            new_tree = self.left_node
        elif self.left_node.right_node.value is None:
            new_tree = self.left_node
            new_tree.right_node = self.right_node
        else:

            node_1 = self.left_node
            node_2 = node_1.right_node
            while node_2.right_node.value is not None:
                node_1 = node_2
                node_2 = node_2.right_node

            new_tree = node_2

            new_tree.right_node = self.right_node

            node_1.right_node = node_2.left_node

            new_tree.left_node = self.left_node      
        if link == '':
            self.value = new_tree.value
            self.left_node = new_tree.left_node
            self.right_node = new_tree.right_node
        elif link == 'L':
            parent.left_node = new_tree
        else:
            parent.right_node = new_tree
        return True
    
    def print_binary_tree(self):
        if self.value is None:
            return
        self._print_binary_tree(0, self.height())

    def _print_binary_tree(self, n, height):
        if n > height:
            return
        if self.value is None:
            print('\n' * (2 ** (height - n + 1) - 1), end = '')
        else:
            self.left_node._print_binary_tree(n + 1, height)
            print('      ' * n, self.value, sep = '')
            self.right_node._print_binary_tree(n + 1, height)
            
    def pre_order_traversal(self):

        if self.value is None:
            return []
        values = [self.value]
        values.extend(self.left_node.pre_order_traversal())
        values.extend(self.right_node.pre_order_traversal())
        return values

    def in_order_traversal(self):

        if self.value is None:
            return []
        values = self.left_node.in_order_traversal()
        values.append(self.value)
        values.extend(self.right_node.in_order_traversal())
        return values

    def post_order_traversal(self):

        if self.value is None:
            return []
        values = self.left_node.post_order_traversal()
        values.extend(self.right_node.post_order_traversal())
        values.append(self.value)
        return values

         






import sys
from random import randint, seed
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
            print('c:',c)
            root.value=value
            root.left_node=BinaryTree()
            root.right_node=BinaryTree()
            try:
                if list[2*c]!=None:
                    print('2*c:',2*c)
                    root.left_node=BinaryTree(list[2*c])
                    self.list_create_tree(root.left_node,list[2*c],list,2*c)
                if list[2*c+1]!=None:
                    #print('2*c+1:',2*c+1)
                    root.right_node=BinaryTree(list[2*c+1])
                    self.list_create_tree(root.right_node,list[2*c+1],list,2*c+1)
            except:
                #pass
                print('error!')
        return

'''
    def list_create_tree(self,root,value,list,c):
        if c <= self.q:
            print('c:',c)
            root.value=value
            try:
                if list[2*c]!=None:
                    #print('2*c:',2*c)
                    self.left_node=BinaryTree(list[2*c])
                    self.list_create_tree(self.left_node,list[2*c],list,2*c)
                    try:
                        if list[2*c+1]!=None:
                            #print('2*c+1:',2*c+1)
                            self.right_node=BinaryTree(list[2*c+1])
                            self.list_create_tree(self.right_node,list[2*c+1],list,2*c+1)
                    except:
                        pass
            except:
                pass
        return
'''





    

            

'''
arg_for_seed=0
nb_of_nodes=2
seed(arg_for_seed)
pq = PriorityQueue()
for _ in range(nb_of_nodes - 1):
    pq.insert(randint(0, nb_of_nodes))
    pq.print_binary_tree()
    print()
pq.insert(randint(0, nb_of_nodes))
pq.print_binary_tree()
'''

'''
a=BinaryTree(2)
a_L=BinaryTree(3)
a_R=BinaryTree(4)
a.left_node=a_L
a.right_node=a_R
a.print_binary_tree()

s=a.size()
print(s)

b=PriorityQueue()
b.print_binary_tree()
b.insert(2)
print(b.pq_list)
b.insert(3)
print(b.pq_list)

b.insert(1)
print(b.pq_list)
b.insert(2)
print(b.pq_list)



arg_for_seed=0
nb_of_nodes=4
seed(arg_for_seed)
pq = PriorityQueue()

print('----')
for _ in range(nb_of_nodes):
    pq.insert(randint(0, nb_of_nodes))
    print(pq.pq_list)

print('----!!!!!------')



pq = PriorityQueue()
pq.insert(1)
print(pq.value)
print(pq.left_node)

'''


b=PriorityQueue()
b.insert(2)
print(b.value)
print(b.left_node)
print(b.right_node)

b.insert(3)
print(b.value)
print(b.left_node)
print(b.right_node)
print(b.pq_list)
b.print_binary_tree()

'''
b.insert(1)
b.insert(2)
print('----!!!!!------')
b.insert(0)
print(b.pq_list)
print(b.value)
#b.print_binary_tree()
#print(b.left_node.value)
#print(b.left_node.left_node.value)

#print(b.right_node.value)
#print(b.right_node.left_node.value)

print('-----')
b.print_binary_tree()



print('111111111111111')
'''
'''
arg_for_seed=0
nb_of_nodes=4
seed(arg_for_seed)
pq = PriorityQueue()
for _ in range(nb_of_nodes):
    pq.insert(randint(0, nb_of_nodes))
    print(pq.pq_list)
    pq.print_binary_tree()
'''

