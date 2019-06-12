import sys
from random import seed, randrange

from queue_adt import *

'''
q=[1,2,3]
a=6
print([6]+[2])
x={1:[1,2,3]}
q=[1][-1]
if q in x:
    print('!')
    print(q)

queue=Queue(10)
print(queue._data)
print(queue._length)
print(len(queue))
queue.enqueue(11)
print(queue._data)
print(len(queue._data))
print(queue._length)
print(len(queue))
print(queue.peek_at_back())
queue.enqueue(4)
print(queue._data)
print(len(queue._data))
print(queue._length)
print(len(queue))
print(queue.peek_at_back())

queue=Queue(1)
#print(queue._data)
#print(queue._length)
#print(len(queue))
queue.enqueue(11)
#print(queue._data)
#print(len(queue._data))
#print(queue._length)
#print(len(queue))
queue.enqueue(4)
#queue.enqueue(3)
print(queue._data)
print(len(queue._data))
print(queue._length)
print('???',len(queue))
print(queue.peek_at_back())

queue=Queue(1)
queue.enqueue(0)
queue.enqueue(1)
queue.enqueue(2)
print(queue._data)
print(queue._length)
print(len(queue._data))
queue.enqueue(5)
print(queue._data)
print(queue._length)
print(len(queue._data))
queue.enqueue(6)
print(queue._data)
print(queue._length)
print(len(queue._data))
queue.enqueue(7)
print(queue._data)
print(queue._length)
print(len(queue._data))



print('------')
queue=Queue(1)
print(queue._data)
print(len(queue._data))
print(queue._length)
print(len(queue))
print('------')
queue.enqueue(4)
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))
print('------')
queue.enqueue(5)
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))
print('------')
queue.enqueue(7)
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))
print('------')
queue.enqueue(11)
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))
print('------')
queue.enqueue(17)
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))

print('~~~~~~~~~~')
queue.dequeue()
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))
print('------')
queue.enqueue([33,22])
print('queue._data:',queue._data)
print('len(queue._data):',len(queue._data))
print('queue._length:',queue._length)
print('front:',queue._front)
print('len(queue):',len(queue))

'''





def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))
#---------------

def directions(i,j,grid,d):
    d1=[]
    if d=='e':
        #东 左
        try:
            if grid[i-1][j] and grid[i-1][j]==1 and (i-1>=0):
                d1.append([i-1,j])
        except:
            pass
        #东 前
        try:
            if grid[i][j+1] and grid[i][j+1]==1:# and (j+1<=2):
        #if grid[i][j+1] and grid[i][j+1]==1 and (j+1<=9):
                d1.append([i,j+1])
        except:
            pass
        #东 右
        try:
            if grid[i+1][j] and grid[i+1][j]==1:
        #if grid[i+1][j] and grid[i+1][j]==1 and (i+1<=9):
                d1.append([i+1,j])
        except:
            pass
    if d=='w':
        #西 左
        try:
            if grid[i+1][j] and grid[i+1][j]==1:
                d1.append([i+1,j])
        except:
            pass
        #西 前
        try:
            if grid[i][j-1] and grid[i][j-1]==1 and (j-1>=0):
                d1.append([i,j-1])
        except:
            pass
        #西 右
        try:
            if grid[i-1][j] and grid[i-1][j]==1 and (i-1>=0):
                d1.append([i-1,j])
        except:
            pass
    if d=='s':
        #南 左
        try:
            if grid[i][j+1] and grid[i][j+1]==1:
                d1.append([i,j+1])
        except:
            pass
        #南 前
        try:
            if grid[i+1][j] and grid[i+1][j]==1:
                d1.append([i+1,j])
        except:
            pass
        #南 右
        try:
            if grid[i][j-1] and grid[i][j-1]==1 and (j-1>=0):
                d1.append([i,j-1])
        except:
            pass
    if d=='n':
        #北 左
        try:
            if grid[i][j-1] and grid[i][j-1]==1 and (j-1>=0):
                d1.append([i,j-1])
        except:
            pass
        #北 前
        try:
            if grid[i-1][j] and grid[i-1][j]==1 and (i-1>=0) :
                d1.append([i-1,j])
        except:
            pass 
        #北 右
        try:
            if grid[i][j+1] and grid[i][j+1]==1:
                d1.append([i,j+1])
        except:
            pass
    if d1==[]:
        return None
    else:
        return d1



def top_left_path(grid):
    if grid[0][0]==0:
        return None
    size=len(grid)-1
    queue=Queue()
    i=0
    j=0
    p=[[i,j]]
    queue.enqueue(p)
    d='e'
    while not queue.is_empty():
        #print('before:',queue._data)
        path=queue.dequeue()
        #print('after:',queue._data)
        #print(path)
        #i j is current position
        i=path[0][0]
        j=path[0][1]
        if i==0 and j==0:
            pass
        else:
        #m n is last position(上一个位置点)
            m=path[1][0]
            n=path[1][1]
            if i==m and j>n:
                d='e'
            elif i==m and j<n:
                d='w'
            elif i>m and j==n:
                d='s'
            elif i<m and j==n:
                d='n'
        if i<=size and j<=size:
        #if i<=9 and j<=9:
            #print('d:',d)
            d1=directions(i,j,grid,d)
            #d1=[[a],[b],[c]]
            if d1:
                for e in reversed(d1):
                    if e in path:
                        continue
                    else:
                        queue.enqueue([e]+path)
    #print(path)
    l=[]
    for k in reversed(path):
        i=k[0]
        j=k[1]
        l.append((i,j))
    return l

def leftmost_longest_path_from_top_left_corner():
    return top_left_path(grid)

















for_seed=7
seed(for_seed)
#grid=[[1,1,1],[1,1,0],[0,1,0]]
grid = [[randrange(2) for _ in range(10)] for _ in range(10)]
print('Here is the grid that has been generated:')
display_grid()

path=leftmost_longest_path_from_top_left_corner()

#path = leftmost_longest_path_from_top_left_corner()

if not path:
    print('There is no path from the top left corner.')
else:
    print(f'The leftmost longest path from the top left corner is: {path})')

