# Randomly generates a binary search tree whose number of nodes
# is determined by user input, with labels ranging between 0 and 999,999,
# displays it, and outputs the maximum difference between consecutive leaves.
#
# Written by *** and Eric Martin for COMP9021

import sys
from random import seed, randrange
from binary_tree_adt import *

# Possibly define some functions

def list_leaf(tree,k):
    if tree.value!=None:
        #print(tree.value)
        if tree.left_node.value!=None:
            #tree=tree.left_node  !!! becareful!!! this is wrong ,because u have changed the root tree
            list_leaf(tree.left_node,k)
        if tree.right_node.value!=None:
            #tree=tree.right_node
            list_leaf(tree.right_node,k)
        if tree.left_node.value==None and tree.right_node.value==None:
            k.append(tree.value)
def max_diff(tree):
    k=[]
    list_leaf(tree,k)
    #print(k)
    diff=[]
    length=len(k)
    if length==1:
        diff.append(0)
    else:
        for i in range(length-1):
            z=abs(k[i]-k[i+1])
            diff.append(z)
    #print(diff)
    maxdiff=max(diff)
    return maxdiff


def max_diff_in_consecutive_leaves(tree):
    return max_diff(tree)
    # Replace pass above with your code
    # Replace pass above with your code


provided_input = input('Enter two integers, the second one being positive: ')
try:
    arg_for_seed, nb_of_nodes = provided_input.split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, nb_of_nodes = int(arg_for_seed), int(nb_of_nodes)
    if nb_of_nodes < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
tree = BinaryTree()
for _ in range(nb_of_nodes):
    datum = randrange(1000000)
    tree.insert_in_bst(datum)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
print('The maximum difference between consecutive leaves is: ', end = '')
print(max_diff_in_consecutive_leaves(tree))
           
