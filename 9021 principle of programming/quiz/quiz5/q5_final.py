# Randomly fills a grid of size 10 x 10 with 0s and 1s and computes:
# - the size of the largest homogenous region starting from the top left corner,
#   so the largest region consisting of connected cells all filled with 1s or
#   all filled with 0s, depending on the value stored in the top left corner;
# - the size of the largest area with a checkers pattern.
#
# Written by *** and Eric Martin for COMP9021

import sys
from random import seed, randint


dim = 10
grid = [[None] * dim for _ in range(dim)]

def display_grid():
    for i in range(dim):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))

# Possibly define other functions

try:
    arg_for_seed, density = input('Enter two nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density = int(arg_for_seed), int(density)
    if arg_for_seed < 0 or density < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
# We fill the grid with randomly generated 0s and 1s,
# with for every cell, a probability of 1/(density + 1) to generate a 0.
for i in range(dim):
    for j in range(dim):
        grid[i][j] = int(randint(0, density) != 0)
print('Here is the grid that has been generated:')
display_grid()
#----------------------------------mycode
#-----
l=list(grid)

#---------------------largest homogenous region
length=dim-1
path=1
i=0
j=0
record=[[i,j]]

def cal(i,j,l):
  global path
  #if i+1<=length and j+1<=length and i-1>=0 and j-1 >=0:
  #if i+1<=length and j+1<=length:
  if i-1>=0:
    if l[i][j]==l[i-1][j]:
      if [i-1,j] in record:
        pass
      elif [i-1,j] not in record:
        record.append([i-1,j])
        path=path+1
        cal(i-1,j,l)
  if j-1>=0:
    if l[i][j]==l[i][j-1]:
      if [i,j-1] in record:
        pass
      elif [i,j-1] not in record:
        record.append([i,j-1])
        path=path+1
        cal(i,j-1,l)
  if j+1<=length:
    if l[i][j]==l[i][j+1]:
      if [i,j+1] in record:
        pass
      elif [i,j+1] not in record:
        record.append([i,j+1])
        path=path+1
        cal(i,j+1,l)
  if i+1<=length:
    if l[i][j]==l[i+1][j]:
      if [i+1,j] in record:
        pass
      elif [i+1,j] not in record:
        record.append([i+1,j])
        path=path+1
        cal(i+1,j,l)

cal(i,j,l)
#print('path:',path)
#size_of_largest_homogenous_region_from_top_left_corner=path
#print(size_of_largest_homogenous_region_from_top_left_corner)
#print(record)
#print(len(record))
'''
#------test
m=4
for i in record:
  a=i[0]
  b=i[1]
  l[a][b]=m
print(l)
for i in range(dim):
    print('   ', ' '.join(str(int(l[i][j])) for j in range(dim)))
'''
#-------------------checkers structer
#length=dim-1
#l=list(grid)
#i=0
#j=4
#q=1
#record_1=[[i,j]]
def cal_2(i,j,l):
  global q
  if i-1>=0:
    if l[i][j]==l[i-1][j]:
      pass
    elif l[i][j]!=l[i-1][j]:
      if [i-1,j] in record_1:
        pass
      else:
        record_1.append([i-1,j]) 
        q=q+1
        cal_2(i-1,j,l)
  if j-1>=0:
    if l[i][j]==l[i][j-1]:
      pass
    elif l[i][j]!=l[i][j-1]:
      if [i,j-1] in record_1:
        pass
      else:
        record_1.append([i,j-1]) 
        q=q+1
        cal_2(i,j-1,l)
  if j+1<=length:
    if l[i][j]==l[i][j+1]:
      pass
    elif l[i][j]!=l[i][j+1]:
      if [i,j+1] in record_1:
        pass
      else:
        record_1.append([i,j+1]) 
        q=q+1
        cal_2(i,j+1,l)
  if i+1<=length:
    if l[i][j]==l[i+1][j]:
      pass
    elif l[i][j]!=l[i+1][j]:
      if [i+1,j] in record_1:
        pass
      else:
        record_1.append([i+1,j]) 
        q=q+1
        cal_2(i+1,j,l) 

#cal_2(i,j,l)
#print(q)
#z=cal_2(0,0,l)
#print(z)



ll = [[1] * dim for _ in range(dim)]
#print(ll)

  
for i in range(length):
  for j in range(length):
    record_1=[[i,j]]
    q=1
    cal_2(i,j,l)
    ll[i][j]=q
    q=0

#print(ll)

lll=[]
for m in ll:
  lll.append(max(m))
#print(lll)
#checkers_structure=max(lll)
#print('checkers_structure:',checkers_structure)
#max_size_of_region_with_checkers_structure=max(lll)
#print(max_size_of_region_with_checkers_structure)










#----------------------------------------------------------
size_of_largest_homogenous_region_from_top_left_corner  = path
# Replace this comment with your code
print('The size_of the largest homogenous region from the top left corner is '
      f'{size_of_largest_homogenous_region_from_top_left_corner}.'
     )

max_size_of_region_with_checkers_structure = max(lll)
# Replace this comment with your code
print('The size of the largest area with a checkers structure is '
      f'{max_size_of_region_with_checkers_structure}.'
     )




            
