#!/usr/bin/python3
#! /usr/bin/env python3

#Because the world is unknow,so I use breadthfirst search to make sure
#the agent can get the gold. But it's a little slowly.
#the program runs in 3 steps
#1.dicovery: go to all boundary that haven't been, to get the biggest view
#2.get_item: if agent see the item, and can go to(use find_path function) it
#  the agent will go to there.if all the item have been get and no boundart
#   haven't been, it will stop. Depend on the item it get to select the path.
#3.if find gold, the agent go back to the startpoint. 

# use chmod +x agent.py
#    ./agent.py -p [Portnumber]
#

from socket import *
import sys, getopt

PORT = 21415 #for idle 
ops, args = getopt.getopt(sys.argv[1:], "p:")
for op , value in ops:
    if op == "-p":
        PORT = int(value)        
        break

def get_view(data):     # scan and get view from current location
    view = [[' ',' ',' ',' ',' ']for _ in range(5)]
    n = 0   
    for i in range(5):
       for j in range(5):             
         if not( i == 2 and j == 2 ):               
            try:
                 view[i][j] = data[n]
                 n += 1
            except IndexError:
                pass
            
    return view

def print_view( view ):
    print("\n+-----+")
    for i in range(5):
        print("|",point = '')
        for j in range(5):
            if i == 2 and j == 2 :
               print('^',end='')
            else: 
               print( str(view[i][j]),end='' )       
        print("|")     
    print("+-----+")

def record_to_world(view): #save the view into the world[][] which is world model
    global world    
    global colum
    global row
    global border_of_world 
    c,r = None,None
    if dirn == 1:       #NORTH  = 1
        c = -2
        colum -= 1
    elif dirn == 3:     #SOUTH  = 3
        c = 2
        colum += 1
    elif dirn == 2:     #WEST   = 2
        r = -2
        row -= 1
    elif dirn == 0:     #EAST   = 0
        r = 2
        row += 1  
    for i in range(-2,3):
        if c == -2:
            world[colum + c][row + i] = view[0][2+i]
        elif c == 2:
            world[colum + c][row - i] = view[0][2+i]
        elif r == -2 :
            world[colum - i][row + r] = view[0][2+i]
        elif r == 2:
            world[colum + i][row + r] = view[0][2+i]
    if colum - 2 < border_of_world['North']:
        border_of_world['North'] = colum -2
    if colum + 2 > border_of_world['South']:
        border_of_world['South'] = colum + 2
    if row - 2 < border_of_world['West']:
        border_of_world['West'] = row - 2
    if row + 2 > border_of_world['East']:
        border_of_world['East'] = row + 2
    if (colum, row) not in have_been:
        have_been.add((colum, row))
 
##----- direction operating function -------
##0.revieve prior view[5][5] from parameter
##1.judge whether can go straight and send command to server
##2.recieve and return view[5][5]
can_go = [' ','o']


def turn_right():
    global sock
    global dirn
    global view
    
    sock.send('r'.encode("UTF-8"))
    if dirn == 0:
        dirn = 3 
    else:
        dirn -= 1
    view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
    return view


def turn_left():
    global sock
    global dirn
    
    sock.send('l'.encode("UTF-8"))
    if dirn == 3:
        dirn = 0
    else:
        dirn += 1
    view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
    return view
    


def forward():
    global sock
    global dirn

    global view
    global stone
    global axo
    global key
    global gold

    if view[1][2] == 'k':
        key = True
    if view[1][2] == 'o':
        stone = True
    if view[1][2] == 'a':
        axo = True
    if view[1][2] == 'g':
        gold = True
        sock.send('f'.encode("UTF-8"))
        view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
        record_to_world(view)
        go_to(search_path(80,80,stone))
        exit()
        
    if view[1][2] == '~':
        stone = False

    if view[1][2] == 'T':
        sock.send('c'.encode("UTF-8"))
        view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
    if view[1][2] == '-':
        sock.send('u'.encode("UTF-8"))
        view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
##    if view[1][2] not in can_go:
##        return False
    
    sock.send('f'.encode("UTF-8"))
    view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
    record_to_world(view)
    

def discover():  #go to the border which have not been
    from copy import deepcopy
    global border_of_world
    item = ['g','o','k','a']
    prior = deepcopy(border_of_world)
    for i in range(border_of_world['North'],border_of_world['South']):
        for j in range(border_of_world['West'],border_of_world['East']):
            if world[i][j] in item:
                temp = search_path(i,j,False)
                if temp :
                    go_to(temp)
            if (i,j) not in have_been and world[i][j] in can_go:
                temp = search_path(i,j,False)
                if temp:
                    go_to(temp)
                   
    if  prior == border_of_world: # no more area to discover
        return
    else:
        discover()
#----------breadth first search-------
class Node():
    def __init__(self):
        self.value = None
        self.father = None
        self.stone = False
        self.colum = None
        self.row = None

    def inherit(self,node): #create new node Inherit from node
        self.father = node
        self.stone = node.stone
        self.colum = node.colum
        self.row = node.row

def search_path(end_colmn,end_row,use_stone): #use breadth first search to find the right position
    global colum
    global row
    global axo
    global gold
    global have_been

    start = Node()
    start.colum = colum
    start.row = row
    start.stone = use_stone
    possibal_path = [start]
    been = [(colum,row)]
    for node in possibal_path:
        can_go = [' ','o','k','a','g']

        if node.colum == end_colmn and node.row == end_row:            
            break
        if node.stone:
            can_go =  can_go + ['~']
        if axo:
            can_go = can_go + ['T']
        if key:
            can_go = can_go + ['-']
        for i in [-1,1]:#breadth frist search check out every place where can go to
            if world[node.colum+i][node.row] in can_go:
                new_node = Node()
                new_node.father = node
                new_node.colum = node.colum+i
                new_node.row = node.row
                new_node.stone = node.stone

                if world[node.colum+i][node.row] == '~':
                    new_node.stone = False
                if (new_node.colum,new_node.row) not in been:
                    been.append((new_node.colum,new_node.row))
                    possibal_path.append(new_node)

            if world[node.colum][node.row+i] in can_go:
                new_node = Node()
                new_node.father = node
                new_node.colum = node.colum
                new_node.row = node.row+i
                new_node.stone = node.stone
                if world[node.colum][node.row+i] == '~':
                    new_node.stone = False
                if (new_node.colum,new_node.row) not in been:
                    been.append((new_node.colum,new_node.row))
                    possibal_path.append(new_node)
    if node.colum != end_colmn or node.row != end_row: #search all possibal path can not get goal
        return False
    result = []
    
    while node.father != None:
        result.append([node.colum,node.row])
        if not (node.colum,node.row) in have_been:
            have_been.add((node.colum,node.row))
        node = node.father
    result.reverse()
    return result 
    

def go_to(result):   # follow the search path go to destination
    global dirn
    global prior_action
    global colum
    global row

    for point in result:
        a = colum - point[0]
        b = row - point[1]
       # print('a={},b={},dirn={}'.format(a,b,dirn))
       # print('colum={},row={},point[0]={},point[1]={}'.format(colum,row,point[0],point[1]))
        if a == -1:
            while dirn != 3:
                turn_right()
            forward()
                
        elif a == 1:
            while dirn != 1:
                turn_right()
            forward()
        elif b == 1:
            while dirn != 2:
                turn_right()
            forward()
        elif b == -1:
            while dirn != 0:
                turn_right()
            forward()
    return
#-------find and get item--------
def get_item():
    global stone
    item = ['g','o','k','a']
    goal = []
    for i in range(border_of_world['North']-5,border_of_world['South']+5):
        for j in range(border_of_world['West']-5,border_of_world['East']+5):
            if world[i][j] in item:
                temp = search_path(i,j,stone)
                if temp:
                    goal.append(temp)
    if len(goal) == 0:
        return
    for p in goal:
        go_to(p)
    
    
                    
                    


#--------------------------------    


##-----global, record current row and colum in world.
##dirn is direction same in record_world()
axo = False
key = False
gold = False
stone = False
colum = 80
row = 80
dirn = 3
world = [[None for _ in range(160)]for _ in range(160)]
#the border of the world have been discoverd
border_of_world = {'West':78,'North':78,'South':82,'East':82}
#record the area '^' have been
have_been = set((colum,row))


HOST = 'localhost'

ADDR = (HOST, PORT) 

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)
view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
for i1 in range(-2,3):
    for j1 in range(-2,3):
            world[colum - i1][row - j1] = view[i1+2][2+j1]
while True:
    discover()
    get_item()