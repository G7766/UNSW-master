## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    #pass # **replace** this line with your code
    i=1
    while abs(i*i-x)>1e-9:
        i=(i+x/i)/2
    #print(i)
    return int(i)


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    #pass # **replace** this line with your code
    x = x_0
    x_new = x_0
    while MAX_ITER>0:
        x=x_new
        x_new = x - f(x)/fprime(x)
        if abs(x-x_new)<EPSILON:
            break
        MAX_ITER = MAX_ITER -1
    
    return x_new

#print(find_root(f, fprime))
#print(f(find_root(f, fprime)))

################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    #pass # **replace** this line with your code    
    #print(tokens)
    stack=[]
    for i in tokens:
        if i!=']':
            stack.append(i)
        else:
            children = []
            #while stack.pop()!='[':
            while stack[-1]!='[':
                children.append(stack.pop()) # pop the latest one save in children
            children.reverse()                # the order is reverse
            stack.pop() # delete '['
            parent = stack.pop()
            
            #if type(parent)!=type(Tree):     # type() 不会认为子类是一种父类类型，不考虑继承关系。
                                              # isinstance() 会认为子类是一种父类类型，考虑继承关系
            
            #if not isinstance(parent,Tree):   # check if the parent and Tree are same type, 
            
            parent = Tree(parent)             # create Tree parent directly
                                            
            for j in children:                # if child is not Tree, create tree and add as child
                if not isinstance(j,Tree):    # if child is Tree, add to parent directly
                    parent.add_child(Tree(j))
                else:
                    parent.add_child(j)
            stack.append(parent)              # the whole parent tree add to statck

    return stack[0]                           # at last there will be only one element in statck
        
        
# help to max_depth
def count_depth(root,count,l):
    l.append(count)
    if len(root.children)>0:
        for child in root.children:
            #print(count)
            count_depth(child,count+1,l)
            
def max_depth(root): # do not change the heading of the function
    #pass # **replace** this line with your code
    l=[]
    count = 1
    count_depth(root,count,l)
    #print(l)
    return max(l)
