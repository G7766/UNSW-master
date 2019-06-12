from random import seed, randint
import sys
from collections import defaultdict


def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))
#------------------------------------------
def find_toppoint(size,dim):
	l=[]
	for i in range(0,dim-size+1):
		for j in range (size-1,dim-size+1):
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
	#print('size:',size)
	l=[]
	#print(q)
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
		#print('!!!!!!!toppoint=',size,'=',q)
		#print('--------')
		#grid=changeto1(grid)
		#print('grid:',grid)
		if sizemax-size>0:
			for i in range(sizemax-size):
				for j in range((len(r[size+i+1]))):
					q[size].remove(r[size+i+1][j])
		print('!!!!!!!!!after=size:',size,'~',q)
		#print('--------')
		numb[size],r[size]=find_triangle(q[size],grid,size)
		print('count:',numb[size])
		print('r[size]:',r[size])
		print('--------')

		d['N'].append([size,numb[size]])
		#print(d)

arg_for_seed, density, dim=0,8,11


seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print('Here is the grid that has been generated:')
display_grid()
# A dictionary whose keys are amongst 'N', 'E', 'S' and 'W',
# and whose values are pairs of the form (size, number_of_triangles_of_that_size),
# ordered from largest to smallest size.


triangles = triangles_in_grid()






