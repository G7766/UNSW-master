from socket import *

def get_view(data):     # scan 5-by-5 wintow around current location
    view = [[' ',' ',' ',' ',' ']for _ in range(5)]
    n = 0   
    for i in range(5):
       for j in range(5):             
         if not( i == 2 and j == 2 ):               
             view[i][j] = data[n]
             n += 1
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


def turn_right(view):
    global sock
    global dirn
    global can_go

    sock.send('r'.encode("UTF-8"))
    if dirn == 0:
        dirn = 3 
    else:
        dirn -= 1
    return get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))


def turn_left(view):
    global sock
    global dirn
    global can_go
    
    sock.send('l'.encode("UTF-8"))
    if dirn == 3:
        dirn = 0
    else:
        dirn += 1
    return get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))


def forward(view):
    global sock
    global dirn
    global can_go
    if view[1][2] not in can_go:
        return False
    
    sock.send('f'.encode("UTF-8"))
    view = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
    record_to_world(view)
    return view

def dicover():  #go to the border which have not been
    from copy import deepcopy
    global border_of_world
    prior = deepcopy(border_of_world)
    for i in range(border_of_world['North'],border_of_world['South']):
        for j in range(border_of_world['West'],border_of_world['East']):
            if (i,j) not in have_been and world[i][j] in can_go:
                go_to(i,j,False)
    if not prior != border_of_world:
        discover()
    else:
        return
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
    
    start = Node()
    start.colum = colum
    start.row = row
    start.stone = use_stone
    possibal_path = [start]
    have_been = [(colum,row)]
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
        for i in [-1,1]:                     #breadth frist search check out every place where can go to
            if world[node.colum+i][node.row] in can_go:
                new_node = Node(node)    
                new_node.colum = node.colum + i

                if world[node.colum+i][node.row] == '~':
                    new_node.stone = False
                if (new_node.colum,new_node.row) not in have_been:
                    have_been.append((new_node.colum,new_node.row))
                    possibal_path.append(new_node)

            if world[node.colum][node.row+i] in can_go:
                new_node = Node(node)
                new_node.row = node.row+i
                if world[node.colum][node.row+i] == '~':
                    new_node.stone = False
                if (new_node.colum,new_node.row) not in have_been:
                    have_been.append((new_node.colum,new_node.row))
                    possibal_path.append(new_node)
    if node.colum != end_colmn or node.row != end_row: #search all possibal path can not get goal
        return False
    result = []
    while node.father != None:
        result.append([node.colum,node.row])       
        node = node.father
    return result.reverse() 
    

def go_to(end,use_stone):   # follow the search path go to destination
    global dirn
    global prior_action
    global colum
    global row
    path = search_path(end[0],end[1],use_stone)
    print(prior_action)

    for point in path:
        a = colum - point[0]
        b = row - point[1]
        print('a={},b={},dirn={}'.format(a,b,dirn))
        print('colum={},row={},point[0]={},point[1]={}'.format(colum,row,point[0],point[1]))
        if a == -1:
            if dirn == 3:
                if world[point[0]][point[1]] == 'T':
                    return 'u'
                if world[point[0]][point[1]] == '-':
                    return 'u'
                
        if a == 1:
            if dirn == 1:
                if world[point[0]][point[1]] == 'T':
                    prior_action = 'c'
                    return 'c'
                if world[point[0]][point[1]] == '-':
                    prior_action = 'u'
                    return 'u'
                prior_action = 'f'
                return 'f'
        if b == 1:
            if dirn == 2:
                if world[point[0]][point[1]] == 'T':
                    prior_action = 'c'
                    return 'c'
                if world[point[0]][point[1]] == '-':
                    prior_action = 'u'
                    return 'u'
                prior_action = 'f'
                return 'f'
        if b == -1:
            if dirn == 0:
                if world[point[0]][point[1]] == 'T':
                    prior_action = 'c'
                    return 'c'
                if world[point[0]][point[1]] == '-':
                    prior_action = 'u'
                    return 'u'
                prior_action = 'f'
                return 'f'
        
        if dirn == 0:
            dirn = 3 
        else:
            dirn -= 1
        prior_action = 'r'
        return 'r'


#--------------------------------    
def hang_out(view):
    while True:
        new_view = forward(view)
        if not new_view:
            break
        view = new_view
    
    view = turn_right(view) # go back
 
    for i in range(30):
        view = turn_right(view)
        view = forward(view)
        if view != False:
            view = turn_right(view)
            while True:
                new_view = forward(view)
                if not new_view:
                    break
                view = new_view
            view = turn_left(view)
            view = forward(view)
            if not view:
                view = turn_right(view)
            view = turn_left(view)
            while True:
                new_view = forward(view)
                if not new_view:
                    break
                view = new_view

##-----global, record current row and colum in world.
##dirn is direction same in record_world()
colum = 40
row = 40
dirn = 3
world = [[None for _ in range(80)]for _ in range(80)]
#the border of the world have been discoverd
border_of_world = {'WEST':38,'North':38,'South':42,'EAST':42}
#record the area '^' have been
have_been = set((colum,row))


HOST = 'localhost'
PORT = 31415
ADDR = (HOST, PORT) 

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)
data = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))


for i in range(200):
    hang_out(data)