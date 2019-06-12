
# coding: utf-8

# In[10]:


L=[[0]]*3
L[0][0]=1
L


# In[22]:


x=10
def f():
    #global x #变全局变量
    x=12
    print(x)
f()
x #还是10


# In[9]:


from random import randrange
random(),random(),random()


# In[43]:


#life game(生命游戏)

from random import random
#grid =[[0]*10]*10
#grid =[[0 for _ in range(10)] for _ in range(10)]
#grid =[[0] * 10 for _ in range(10)]
grid =[[0] * 12 for _ in range(12)]
#density= 0.1
density= 0.4

for i in range(1,11):
    for j in range(1,11):
        if random() < density:
            grid[i][j]=1
new_grid=[[0]*12 for _ in range(12)]


def next_generation():
    global grid
    for i in range(1,11):
        for j in range(1,11):
            # number of neighbors of grid[i][j] set to 1
            nb_of_neighbours = sum((grid[i-1][j-1],
                                   grid[i-1][j],
                                   grid[i-1][j+1],
                                   grid[i][j-1],
                                   grid[i][j+1],
                                   grid[i+1][j-1],
                                   grid[i+1][j],
                                   grid[i+1][j+1]))
            if nb_of_neighbours == 3 or (nb_of_neighbours==2 and grid[i][j]):
                new_grid[i][j]=1
            else:
                new_grid[i][j]=0
    grid = new_grid 
        
        
def print_grid():
    #for i in range(10):
    for i in range(1,11):
        #print(''.join(grid[i]))   #wrong
        print(' '.join(str(e) for e in grid[i][1:11]))
print_grid()
print('\n')
next_generation()
print_grid()
next_generation()


# In[11]:


L=[[0 for _ in range(10)]]*10
L

