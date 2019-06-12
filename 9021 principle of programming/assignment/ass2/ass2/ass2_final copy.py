import sys
import os
from copy import deepcopy


class Frieze:
	#input file name
	def __init__(self,file):
		try:
			with open(file,'r') as file:
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
				#print('height:',height)
				#print('length:',length)
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


def horizontal_reflection(b_grid,period):
	height=len(b_grid)
	length=len(b_grid[0])
	grid1=[]
	grid2=[]
	#---even
	if height%2==0:
		horizontal_line_1=int(height/2)
		horizontal_line_2=horizontal_line_1+1
		#print(horizontal_line_1)
		#print(horizontal_line_2)
		#---grid1
		for j in range(horizontal_line_1):
			grid1.append([])
			for i in range(period):
				grid1[j].append(b_grid[j][i])
		print('grid1:')
		display_grid(grid1)
		#---grid2
		for j in range(horizontal_line_2-1,height):
			grid2.append([])
			for i in range(period):
				grid2[j-(horizontal_line_2-1)].append(b_grid[j][i])
		print('grid2:')
		display_grid(grid2)
	#----odd
	if height%2!=0:
		horizontal_line_1=height//2
		horizontal_line_2=horizontal_line_1+1
		#print(horizontal_line_1)
		#print(horizontal_line_2)
		#---grid1
		for j in range(horizontal_line_1+1):
			grid1.append([])
			for i in range(period):
				grid1[j].append(b_grid[j][i])
		print('grid1:')
		display_grid(grid1)
		#---grid2
		for j in range(horizontal_line_2-1,height):
			grid2.append([])
			for i in range(period):
				grid2[j-(horizontal_line_2-1)].append(b_grid[j][i])
		print('grid2:')
		display_grid(grid2)
	#----
	#flag=0
	#while flag!=1:
	count=0
	for j in range(len(grid1)):
		for i in range(len(grid1[0])):
			# |
			if grid1[j][i][-1]=='1':
				try:
					if grid2[-j][i][-1]=='1':
						pass
					else:
						print(grid1[j][i])
						print('i:',i,'j:',j)
						count=count+1
				except:
					print()
					print(grid1[j][i])
					print('false')
			# /
			if grid1[j][i][-2]=='1':
				try:
					if grid2[-j-1][i][-4]=='1':
						pass
					else:
						print(grid1[j][i])
						print('i:',i,'j:',j)
						count=count+1
				except:
					print()
					print(grid1[j][i])
					print('false')
			# --
			if grid1[j][i][-3]=='1':
				try:
					if grid2[-j-1][i][-3]=='1':
						pass
					else:
						print(grid1[j][i])
						print('i:',i,'j:',j)
						count=count+1
				except:
					print()
					print(grid1[j][i])
					print('false')
			# \
			if grid1[j][i][-4]=='1':
				try:
					if grid2[-j-1][i][-2]=='1':
						pass
					else:
						print(grid1[j][i])
						print('i:',i,'j:',j)
						count=count+1
				except:
					print()
					print(grid1[j][i])
					print('false')
	print(count)
	if count==0:
		return 1
	else:
		return 0


def if_is_vertical_reflection(grid1,period):
	height=len(grid1)
	length=len(grid1[0])
	#not on the verticleline
	value=0
	for j in range(height):
		for i in range(0,period-1):
			#  |
			try:
				if grid1[j][i][-1]=='1':
					if grid1[j][-1-i][-1]=='1':
						pass
					else:
						#print('false')
						#print('j:',j,'i:',i)
						#print(grid1[j][i])
						value +=1
					#print('false')
			except:
				value +=1
				#print()
				#print('j:',j,'i:',i)
				#print(grid1[j][i])
				#print('!!!???')
			#  /
			try:
				if grid1[j][i][-2]=='1':
					try:
						if grid1[j-1][-2-i][-4]=='1':
							pass
						else:
							#print('false')
							#print('j:',j,'i:',i)
							#print(grid1[j][i])
							value +=1
							#print('false')
					except:
						value +=1
						#print()
						#print(grid1[j][i])
						#print('no this element')
			except:
				value +=1
				#print()
				#print('j:',j,'i:',i)
				#print(grid1[j][i])
				#print('!!!')
			#  -
			try:
				if grid1[j][i][-3]=='1':
					try:
						if grid1[j][-2-i][-3]=='1':
							pass
						else:
							#print('false')
							#print('j:',j,'i:',i)
							#print(grid1[j][i])
							value +=1
							#print('false')
					except:
						value +=1
						#print()
						#print('j:',j,'i:',i)
						#print(grid1[j][i])
						#print('no this element')
			except:
				value +=1
				#print()
				#print('j:',j,'i:',i)
				#print(grid1[j][i])
				#print('!!!')
			#  \
			try:
				if grid1[j][i][-4]=='1':
					try:
						if grid1[j+1][-2-i][-2]=='1':
							pass
						else:
							#print('false')
							#print('j:',j,'i:',i)
							#print(grid1[j][i])
							value +=1
							#print('false')
					except:
						value +=1
						#print()
						#print('j:',j,'i:',i)
						#print(grid1[j][i])
						#print('no this element')
			except:	
				value +=1
				#print()
				#print('j:',j,'i:',i)
				#print(grid1[j][i])
				#print('!!!')
	#print('value:',value)
	if value==0:
		return 1
	else:
		return 0


def vertical_reflection(b_grid,period):
	height=len(b_grid)
	length=len(b_grid[0])
	#  period/2 <= vertical_line <= 1.5* period
	final=0
	line=0
	while line<=period and final==0:
		grid1=[]
		grid2=[]
		grid1_reverse=[]
		grid2_reverse=[]
	#verticleline is not in line
		for j in range(height):
			grid1.append([])
			for i in range(line,line+period):
				grid1[j].append(b_grid[j][i])
		#print('grid1:')
		#display_grid(grid1)
		a=if_is_vertical_reflection(grid1,period)
		#print('a:',a)

		#verticleline is in line
		for j in range(height):
			grid2.append([])
			for i in range(line,line+period+1):
				grid2[j].append(b_grid[j][i])
		#print('line:',line)
		#print('grid2:')
		#display_grid(grid2)
		b=if_is_vertical_reflection(grid2,period)
		#print('b:',b)
		if a==1 or b==1:
			final=1
			break
		line +=1
		#print('line:',line)
	if final==1:
		#print('verticleline:',line-1)
		return 1
	else:
		return 0


def glided_horizontal_reflection(b_grid,period):
	height=len(b_grid)
	length=len(b_grid[0])
	grid1=[]
	grid2=[]
	#---even
	if height%2==0:
		horizontal_line_1=int(height/2)
		horizontal_line_2=horizontal_line_1+1
		#print(horizontal_line_1)
		#print(horizontal_line_2)
		#---grid1
		for j in range(horizontal_line_1):
			grid1.append([])
			for i in range(period):
				grid1[j].append(b_grid[j][i])
		#print('grid1:')
		#display_grid(grid1)
		#---grid2
		for j in range(horizontal_line_2-1,height):
			grid2.append([])
			for i in range(period):
				grid2[j-(horizontal_line_2-1)].append(b_grid[j][i])
		#print('grid2:')
		#display_grid(grid2)
	#----odd
	if height%2!=0:
		horizontal_line_1=height//2
		horizontal_line_2=horizontal_line_1+1
		#print(horizontal_line_1)
		#print(horizontal_line_2)
		#---grid1
		for j in range(horizontal_line_1+1):
			grid1.append([])
			for i in range(period):
				grid1[j].append(b_grid[j][i])
		#print('grid1:')
		#display_grid(grid1)
		#---grid2
		for j in range(horizontal_line_2-1,height):
			grid2.append([])
			for i in range(period):
				grid2[j-(horizontal_line_2-1)].append(b_grid[j][i])
		#print('grid2:')
		#display_grid(grid2)
	grid3=[]
	# move period/2
	for j in range(len(grid1)):
		grid3.append([])
		for i in range(period//2,len(grid1[0])):
			grid3[j].append(grid1[j][i])

	for j in range(len(grid1)):
		for i in range(period//2):
			grid3[j].append(grid1[j][i])
	#print('grid3')
	#display_grid(grid3)
	reshape_grid=deepcopy(grid3)
	if height%2==0:
		for i in grid2:
			reshape_grid.append(i)
	if height%2!=0:
		reshape_grid.pop()
		for i in grid2:
			reshape_grid.append(i)
	#print('reshape_grid')
	#display_grid(reshape_grid)
	a=horizontal_reflection(reshape_grid,period)
	return a

def if_is_rotation_reflection(grid1,period):
	height=len(grid1)
	length=len(grid1[0])
	grid_x=[]
	for j in range(height):
		grid_x.append([])
		for i in range(period):
			grid_x[j].append(grid1[j][i])
	#print('grid_x:')
	#display_grid(grid_x)
	final=0
	line=0
	while line<=period and final==0:
		value=0
		grid_y=[]
		for j in range(height):
			grid_y.append([])
			for i in range(line,line+period):
				grid_y[j].append(grid1[j][i])
		#print('grid_y:')
		#display_grid(grid_y)
		for j in range(height):
			for i in range(period):
				#  |
				try:
					if grid_x[j][i][-1]=='1':
						if grid_y[-j][-i][-1]=='1':
							pass
						else:
							#print('j:',j,' ', 'i:',i)
							#print('|')
							value +=1
				except:
					#print('j:',j,' ', 'i:',i)
					#print('?|')
					value +=1
				#  /
				try:
					if grid_x[j][i][-2]=='1':
						try:
							if grid_y[-j][-1-i][-2]=='1':
								pass
							else:
								#rint('/')
								value +=1
						except:
							#print('?/')
							value +=1

				except:
					#print('??/')
					value +=1

				#  -
				try:
					if grid_x[j][i][-3]=='1':
						try:
							if grid_y[-1-j][-1-i][-3]=='1':
								pass
							else:
								#print('-')
								value +=1
						except:
							#print('?-')
							value +=1

				except:
					#print('??-')
					value +=1

				#  \
				try:
					if grid_x[j][i][-4]=='1':
						try:
							if grid_y[-2-j][-1-i][-4]=='1':
								pass
							else:
								#print('\\')
								value +=1

						except:
							#print('?\\')
							value +=1
				except:
					#print('??\\')	
					value +=1
		#print('value:',value)
		if value==0:
			#print('line@@@:',line)
			final=1
		else:
			line +=1

	if final==1:
		return 1
	else:
		return 0


def rotation_reflection(b_grid,period):
	height=len(b_grid)
	length=len(b_grid[0])
	line=0
	final=0
	#while line<=period and final==0:
	while line==0 and final==0:
		grid1=[]
		# grid1
		for j in range(height):
			grid1.append([])
			for i in range(line,line+2*period):
				grid1[j].append(b_grid[j][i])
		#print('grid1:')
		#display_grid(grid1)
		#print('line:',line)
		z=if_is_rotation_reflection(grid1,period)
		#print(z)
		#print(line)
		if z==1:
			final=1
			#print('z:',z)
			return 1
		else:
			line +=1
	return 0

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





period=period(grid)
print('period:',period)
h=horizontal_reflection(b_grid,period)
print('h:',h)
v=vertical_reflection(b_grid,period)
print('v:',v)
g=glided_horizontal_reflection(b_grid,period)
print('g:',g)