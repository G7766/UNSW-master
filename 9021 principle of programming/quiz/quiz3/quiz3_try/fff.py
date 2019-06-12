# Randomly generates a grid with 0s and 1s, whose dimension is controlled by user input,
# as well as the density of 1s in the grid, and finds out, for a given direction being
# one of N, E, S or W (for North, East, South or West) and for a given size greater than 1,
# the number of triangles pointing in that direction, and of that size.
#
# Triangles pointing North:
# - of size 2:
#   1
# 1 1 1
# - of size 3:
#     1
#   1 1 1
# 1 1 1 1 1
#
# Triangles pointing East:
# - of size 2:
# 1
# 1 1
# 1
# - of size 3:
# 1
# 1 1
# 1 1 1 
# 1 1
# 1
#
# Triangles pointing South:
# - of size 2:
# 1 1 1
#   1
# - of size 3:
# 1 1 1 1 1
#   1 1 1
#     1
#
# Triangles pointing West:
# - of size 2:
#   1
# 1 1
#   1
# - of size 3:
#     1
#   1 1
# 1 1 1 
#   1 1
#     1
#
# The output lists, for every direction and for every size, the number of triangles
# pointing in that direction and of that size, provided there is at least one such triangle.
# For a given direction, the possble sizes are listed from largest to smallest.
#
# We do not count triangles that are truncations of larger triangles, that is, obtained
# from the latter by ignoring at least one layer, starting from the base.
#
# Written by *** and Eric Martin for COMP9021


from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))
#------------------------------------------
def find_toppoint(size,dim):
	l=[]
	for i in range(0,dim-size+1):           #6
		for j in range (size-1,dim-size+1):     #5,6
			if int(grid[i][j])!=0:
				#print('i:',i,'j:',j,'q')
				l.append([i,j])
			else:
				#print('??')
				pass
	return l

def changeto1(q):
	for i in range(len(q)):
		for j in range(len(q)):
			if q[i][j]!=0:
				q[i][j]=1
	return q

def find_triangle(q,grid,size):
	count=0
	count1=0
	print('size:',size)
	l=[]
	print(q)
	for m in range(len(q)):
		#print(type(q))
		raw=q[m][0]
		cul=q[m][1]
		for h in range(1,size):
			if grid[raw+h][cul-h:cul+h+1]==[1]*(2*h+1):
				count=count+1
				#print(count)
				if count==size-1:
					count1=count1+1
					count=0
					l.append([raw,cul])

			else:
				count=0
				break
	return count1,l

def reverse_dirction(k):
	k.reverse()
	return k

#是旋转加对折
def rotation90(z):
	for i in range(len(z)):
		for j in range(i,len(z)):
			temp=z[i][j]
			z[i][j]=z[j][i]
			z[j][i]=temp
	return z
#删除size长度下，个数为0的列
def dellist(ee):
	ee1=[]
	for i in range(len(ee)):
		print(i)
		if ee[i][1]==0:
			ee1.append(ee[i])
	print(ee1)
	for i in range(len(ee1)):
		ee.remove(ee1[i])
	print(ee)
	return ee
def delnumb(d):
	nn=d.get('N')
	ss=d.get('S')
	ww=d.get('W')
	ee=d.get('E')
	nn=dellist(nn)
	ss=dellist(ss)
	ww=dellist(ww)
	ee=dellist(ee)
	d['N']=nn
	d['S']=ss
	d['W']=ww
	d['E']=ee
	if d['N']==[]:
		d.pop('N')
	if d['S']==[]:
		d.pop('S')
	if d['W']==[]:
		d.pop('W')
	if d['E']==[]:
		d.pop('E')
	return d
#-----------------------------
def triangles_in_grid():
	global grid
	d={'N':[],'S':[],'W':[],'E':[]}
	sizemax=(dim+1)//2
	#print(sizemax)
	print('---------------North---------')
	grid=changeto1(grid)
	#print('grid:',grid)
	display_grid()
	pp=range(2,sizemax+1)
	r=[0]*(sizemax+1)
	numb=[0]*(sizemax+1)
	q=[0]*(sizemax+1)
	# direction 'N'
	for size in reversed(pp):
		#print('????size:',size)
		q[size]=find_toppoint(size,dim)
		print('toppoint={size}:',q)
		#print('--------')
		#grid=changeto1(grid)
		#print('grid:',grid)
		if size<sizemax:
			for i in range(len(r[size+1])):
				q[size].remove(q[size+1][i])

		#print('--------')
		numb[size],r[size]=find_triangle(q[size],grid,size)
		#print('count:',numb[size])
		#print(r[size])
		#print('--------')

		d['N'].append([size,numb[size]])
		#print(d)

	

	# direction 'S'
	print('---------------South---------')
	#print('grid:',grid)
	#display_grid()
	grid=reverse_dirction(grid)
	#print('-----------Sgrid:',grid)
	#print('Here is the grid that has been generated:')
	display_grid()
	pp=range(2,sizemax+1)
	r=[0]*(sizemax+1)
	numb=[0]*(sizemax+1)
	q=[0]*(sizemax+1)
	# direction ''
	for size in reversed(pp):
		#print('????size:',size)
		q[size]=find_toppoint(size,dim)
		#print('toppoint={size}:',q)
		#print('--------')
		#grid=changeto1(grid)
		#print('grid:',grid)
		if size<sizemax:
			for i in range(len(r[size+1])):
				q[size].remove(r[size+1][i])

		#print('--------')
		numb[size],r[size]=find_triangle(q[size],grid,size)
		#print('count:',numb[size])
		#print(r[size])
		#print('--------')

		d['S'].append([size,numb[size]])
		#print(d)




	# direction 'E'
	print('---------------West---------')
	grid=rotation90(grid)
	#print('-----------Egrid:',grid)
	display_grid()

	pp=range(2,sizemax+1)
	r=[0]*(sizemax+1)
	numb=[0]*(sizemax+1)
	q=[0]*(sizemax+1)
	# direction ''
	for size in reversed(pp):
		#print('????size:',size)
		q[size]=find_toppoint(size,dim)
		#print('toppoint={size}:',q)
		#print('--------')
		#grid=changeto1(grid)
		#print('grid:',grid)
		if size<sizemax:
			for i in range(len(r[size+1])):
				q[size].remove(r[size+1][i])

		#print('--------')
		numb[size],r[size]=find_triangle(q[size],grid,size)
		#print('count:',numb[size])
		#print(r[size])
		#print('--------')

		d['W'].append([size,numb[size]])
		#print(d)




	# direction 'W'
	print('---------------East---------')
	#print('grid:',grid)
	#display_grid()
	grid=reverse_dirction(grid)
	#print('-----------Sgrid:',grid)
	#print('Here is the grid that has been generated:')
	display_grid()
	pp=range(2,sizemax+1)
	r=[0]*(sizemax+1)
	numb=[0]*(sizemax+1)
	q=[0]*(sizemax+1)
	# direction ''
	for size in reversed(pp):
		#print('????size:',size)
		q[size]=find_toppoint(size,dim)
		#print('toppoint={size}:',q)
		#print('--------')
		#grid=changeto1(grid)
		#print('grid:',grid)
		if size<sizemax:
			for i in range(len(r[size+1])):
				q[size].remove(r[size+1][i])

		#print('--------')
		numb[size],r[size]=find_triangle(q[size],grid,size)
		#print('count:',numb[size])
		#print(r[size])
		#print('--------')
		print('---------------------------')
		d['E'].append([size,numb[size]])
		print(d)
	d=delnumb(d)
	print(d)
	return d
#----------------------- Replace return {} above with your code

# Possibly define other functions

try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are amongst 'N', 'E', 'S' and 'W',
# and whose values are pairs of the form (size, number_of_triangles_of_that_size),
# ordered from largest to smallest size.
triangles = triangles_in_grid()
for direction in sorted(triangles, key = lambda x: 'NESW'.index(x)):
    print(f'\nFor triangles pointing {direction}, we have:')
    for size, nb_of_triangles in triangles[direction]:
        triangle_or_triangles = 'triangle' if nb_of_triangles == 1 else 'triangles'
        print(f'     {nb_of_triangles} {triangle_or_triangles} of size {size}')