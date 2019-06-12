import sys
import os
from copy import deepcopy

#---------function
def display_grid(grid):
    for i in range(len(grid)):
        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))




#file_name=input('Which data file do you want to use?')
directory_name='/Users/g/desktop/'
file_name='frieze_1.txt'

try:
	with open(directory_name+file_name,'r') as file:
		grid=[]
		for line in file:
			line=line.strip('')
			line=line.split()
			#print(line)
			z=[]
			for x in line:
				z.append(int(x))
			if z!=[]:
				grid.append(z)
	height=len(grid)
	length=len(grid[0])
	print('height:',height)
	print('length:',length)
	if length>=5 and length<=51:
		pass
	else:
		print('The length is not correct!')
		sys.exit()
	if height>=3 and height<=17:
		pass
	else:
		print('The height is not correct!')
		sys.exit()
except IOError:
	print('Incorrect input.')
	sys.exit()
except ValueError:
	print('Incorrect input.')
	sys.exit()
print('--------------')
print('--------------')
print('This is grid list:')
print(grid)
print('--------------')
print('--------------')
print('Here is the grid that has been generated:')
display_grid(grid)
print('--------------')
print('--------------')
print('Here is binary base grid:')
b_grid=deepcopy(grid)
#print(b_grid)
for i in range(len(b_grid)):
	for j in range(len(b_grid[i])):
		n=bin(b_grid[i][j])
		if len(n)==3:
			a='0'
			n=a+n
		b_grid[i][j]=n[-4:]

print()
print(b_grid)
display_grid(b_grid)
print('--------------')
print('--------------')

#qualify a frieze and period
def period(grid):
	height=len(grid)
	length=len(grid[0])
	print('height:',height)
	print('length:',length)
	period=1
	grid1=[1]
	grid2=[2]
	while grid1!=grid2:
		grid1=[]
		grid2=[]
		for j in range(height):
			#print('j:',j)
			for i in range(0,period):
				#print(i)
				grid1.append(grid[j][i])
		#print(grid1)
		for j in range(height):
			for i in range(period,period+period):
				grid2.append(grid[j][i])
		#print(grid2)
		period +=1

	return period-1
			
'''
def n_s_line(i,j,l,grid):
	if grid[i][j][-1]=='1':
		l.append((i,j)) 
'''

def consequence(l,m):
	length=len(l)
	c=0
	for x in range(legnth):
		if l[x][-1]+1=l[x][-1]:
			c +=1
		else:
			m.append([l[:c]])
			del l[:c]
			consequence(l,m)


	


hh=len(b_grid)
ll=len(b_grid[0])

with open('xxx.tex','w') as file_name:
	print('\\documentclass{article}\n'
		  '\\usepackage{tikz}\n'
		  '\\usepackage[margin=0cm]{geometry}\n'
		  '\\pagestyle{empty}\n'
		  '\n'
		  '\\begin{document}\n'
		  '\n'
		  '\\vspace*{\\fill}\n'
		  '\\begin{center}\n'
		  '\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]',file=file_name
		  )
	print('% North to South lines\n',file=file_name)

	for i in range(ll):
		l=[]
		for j in range(hh):
			if b_grid[j][i][-1]=='1':
				l.append([i,j])
		m=[]
		print(l)
























