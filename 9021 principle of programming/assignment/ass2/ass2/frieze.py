import sys
import os
from copy import deepcopy
from operator import itemgetter

class FriezeError(Exception):
    def __init__(self, error = 'Incorrect input.'):
        Exception.__init__(self, error)
def display_grid(grid):
	    for i in range(len(grid)):
	        print('   ', ' '.join(str(grid[i][j]) for j in range(len(grid[0]))))


def _period(grid):
	height=len(grid)
	length=len(grid[0])
	#print('height:',height)
	#print('length:',length)
	period=1
	grid1=[1]
	grid2=[2]
	flag=0
	while period<=length//2 and grid1!=grid2:
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
				#print('!!!!!period:',period)
				grid2.append(grid[j][i])
		#print(grid2)
		if grid1==grid2:
			return period
		else:
			period +=1
	return 0

#-----------------------------------
#		part2 function
#-----------------------------------

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
						#print(grid1[j][i])
						#print('i:',i,'j:',j)
						count=count+1
				except:
					count=count+1
					#print()
					#print(grid1[j][i])
					#print('false')
			# /
			if grid1[j][i][-2]=='1':
				try:
					if grid2[-j-1][i][-4]=='1':
						pass
					else:
						#print(grid1[j][i])
						#print('i:',i,'j:',j)
						count=count+1
				except:
					count=count+1
					#print()
					#print(grid1[j][i])
					#print('false')
			# --
			if grid1[j][i][-3]=='1':
				try:
					if grid2[-j-1][i][-3]=='1':
						pass
					else:
						#print(grid1[j][i])
						#print('i:',i,'j:',j)
						count=count+1
				except:
					count=count+1
					#print()
					#print(grid1[j][i])
					#print('false')
			# \
			if grid1[j][i][-4]=='1':
				try:
					if grid2[-j-1][i][-2]=='1':
						pass
					else:
						#print(grid1[j][i])
						#print('i:',i,'j:',j)
						count=count+1
				except:
					count=count+1
					#print()
					#print(grid1[j][i])
					#print('false')
	#print(count)
	if count==0:
		return 1
	else:
		return 0
#horizontal_reflection(b_grid,3)



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

#----------------------------------------------------



#------------------------------------
#		part3(function)
#------------------------------------

def continuous1(l):
	j=0
	q=[]
	for i,item in enumerate(l):
		if i > 0:
			if l[i][-1]!=l[i-1][-1]+1:
				#print(i)
				#print(j)
				q.append(l[j:i])
				#print(q)
				j=i
	q.append(l[j:])
	return q
def continuous2(l):
	j=0
	q=[]
	for i,item in enumerate(l):
		if i > 0:
			if l[i][0]!=l[i-1][0]+1:
				#print(i)
				#print(j)
				q.append(l[j:i])
				#print(q)
				j=i
	q.append(l[j:])
	return q


def dignoal_continuous_t1(grid,j,i,l):
	try:
		if grid[j+1][i-1][-2]=='1':
			m=[j+1,i-1]
			if m not in l:
				l.append([j+1,i-1])
				l=dignoal_continuous_t1(grid,j+1,i-1,l)
		else:
			return l
	except:
		return l

def dignoal_continuous_cc1(l):
	j=0
	q=[]
	for i,item in enumerate(l):
		if i > 0:
			if l[i][0]!=l[i-1][0]+1 or l[i][1]!=l[i-1][1]-1:
				#print(i)
				#print(j)
				q.append(l[j:i])
				#print(q)
				j=i
	q.append(l[j:])
	return q

def dignoal_continuous_t2(grid,j,i,l):
	try:
		if grid[j+1][i+1][-4]=='1':
			m=[j+1,i+1]
			if m not in l:
				l.append([j+1,i+1])
				l=dignoal_continuous_t2(grid,j+1,i+1,l)
		else:
			return l
	except:
		return l
def dignoal_continuous_cc2(l):
	j=0
	q=[]
	for i,item in enumerate(l):
		if i > 0:
			if l[i][0]!=l[i-1][0]+1 or l[i][1]!=l[i-1][1]+1:
				#print(i)
				#print(j)
				q.append(l[j:i])
				#print(q)
				#print('j:',j,'i:',i)
				j=i
			
	q.append(l[j:])
	return q


#--------------------------------------------










class Frieze:
	#input file name
	def __init__(self,file):
		directory_name='/Users/g/desktop/9021_ass2_test/'
		try:
			with open(directory_name+file,'r') as file:
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
			if length>=5 and length<=51:
				pass
			else:
				raise FriezeError('Incorrect input.')
				sys.exit()
			if height>=3 and height<=17:
				pass
			else:
				raise FriezeError('Incorrect input.')
				sys.exit()

			for j in range(height):
				if len(grid[j])!=length:
					raise FriezeError('Incorrect input.')
					sys.exit()

			for j in range(height):
				for i in range(length):
					if int(grid[j][i]) not in [x for x in range(16)]:
						raise FriezeError('Incorrect input.')
						sys.exit()

		#except IOError:
			#print('a')
			#print('Incorrect input.')
			#sys.exit()
		except ValueError:
			raise FriezeError('Incorrect input.')
			sys.exit()
		#except FileNotFoundError:
			#print('a')
			#sys.exit()


		# let grid become like '0000'
		b_grid=deepcopy(grid)
		for i in range(len(b_grid)):
			for j in range(len(b_grid[i])):
				n=bin(b_grid[i][j])
				if len(n)==3:
					a='0'
					n=a+n
				b_grid[i][j]=n[-4:]


		#--
		'''
		print('Here is the grid that has been generated:')
		display_grid(grid)
		print('')
		print('Here is the b_grid that has been generated:')
		display_grid(b_grid)
		'''
		#print()
		#print(b_grid)
		#display_grid(b_grid)
		
		period=_period(grid)

		height=len(b_grid)
		length=len(b_grid[0])
		#1 --verticle bond--
		for j in range(height):
			if b_grid[j][0][-1]=='1':
				if b_grid[j][-1][-1]=='1':
					pass
				else:
					#print('j:',j)
					raise FriezeError('Input does not represent a frieze.')
					sys.exit()
		for j in range(height):
			if b_grid[j][-1][-1]=='1':
				if b_grid[j][0][-1]=='1':
					pass
				else:
					#print('j:',j)
					raise FriezeError('Input does not represent a frieze.')
					sys.exit()
		#2 --horizontal bond--
		for i in range(length):
			if b_grid[0][i][-3]=='1':
				if b_grid[-1][i][-3]=='1':
					pass
				else:
					raise FriezeError('Input does not represent a frieze.')
					sys.exit()
		for i in range(length):
			if b_grid[-1][i][-3]=='1':
				if b_grid[0][i][-3]=='1':
					pass
				else:
					raise FriezeError('Input does not represent a frieze.')
					sys.exit()
		#3 --top out of bond--
		for i in range(length):
			if b_grid[0][i][-2]=='1':
				raise FriezeError('Input does not represent a frieze.')
				sys.exit()
		#4 --botton out of bond--
		for i in range(length):
			if b_grid[-1][i][-4]=='1':
				raise FriezeError('Input does not represent a frieze.')
				sys.exit()
		#5 --crossing--
		for j in range(height-1):
			for i in range(length):
				if b_grid[j][i][-4]=='1' and b_grid[j+1][i][-2]=='1':
					raise FriezeError('Input does not represent a frieze.')
					sys.exit()
		#6 --period--
		if period<2:
			raise FriezeError('Input does not represent a frieze.')
			sys.exit()
		
		self.file=file
		self.grid=grid
		self.b_grid=b_grid
		self.period=period


	def analyse(self):
		h=horizontal_reflection(self.b_grid,self.period)
		#print('h:',h)
		v=vertical_reflection(self.b_grid,self.period)
		#print('v:',v)
		g=glided_horizontal_reflection(self.b_grid,self.period)
		#print('g:',g)
		r=rotation_reflection(self.b_grid,self.period)
		#print('r:',r)
		if h==0 and v==0 and g==0 and r==0:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation only.')
		if h==0 and v==1 and g==0 and r==0:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and vertical reflection only.')
		if h==1 and v==0 and g==0 and r==0:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and horizontal reflection only.')
		if h==0 and v==0 and g==1 and r==0:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and glided horizontal reflection only.')
		if h==1 and v==0 and g==0 and r==0:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and horizontal reflection only.')
		if h==0 and v==0 and g==0 and r==1:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation\n        and rotation only.')
		if h==0 and v==1 and g==1 and r==1:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        glided horizontal and vertical reflections, and rotation only.')
		if h==1 and v==1 and g==0 and r==1:
			print(f'Pattern is a frieze of period {self.period} that is invariant under translation,\n        horizontal and vertical reflections, and rotation only.')


	def display(self):
		grid=self.grid
		b_grid=self.b_grid
		period=self.period
		file=self.file.name[:-4]+'.tex'
		#print(file)
		hh=len(b_grid)
		ll=len(b_grid[0])
		
		with open(file,'w') as file_name:
			print('\\documentclass[10pt]{article}\n'
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
			print('% North to South lines',file=file_name)
			for i in range(ll):
				l=[]
				for j in range(hh):
					if b_grid[j][i][-1]=='1':
						l.append((i,j))
				#print(l)
				q=continuous1(l)
				if q==[[]]:
					pass
				else:
					for i in range(len(q)):
						print(f'    \draw ({q[i][0][0]},{q[i][0][1]-1}) -- ({q[i][-1][0]},{q[i][-1][1]});',file=file_name)
			
			print('% North-West to South-East lines',file=file_name)
			l=[]
			for j in range(hh):
				for i in range(ll):
					try:
						if b_grid[j][i][-4]=='1':
							m=[j,i]
							if m not in l:
								l.append([j,i])
								dignoal_continuous_t2(b_grid,j,i,l)
						#print(l)
					except:
						break
			l=dignoal_continuous_cc2(l)
			#print('l:',l)
			if l==[[]]:
				pass
			else:
				for i in range(len(l)):
					print(f'    \draw ({l[i][0][1]},{l[i][0][0]}) -- ({l[i][-1][1]+1},{l[i][-1][0]+1});',file=file_name)



			print('% West to East lines',file=file_name)
			for j in range(hh):
				l=[]
				for i in range(ll):
					if b_grid[j][i][-3]=='1':
						l.append((i,j))
				q=continuous2(l)
				if q==[[]]:
					pass
				else:
					for i in range(len(q)):
						print(f'    \draw ({q[i][0][0]},{q[i][0][1]}) -- ({q[i][-1][0]+1},{q[i][-1][1]});',file=file_name)
			
			print('% South-West to North-East lines',file=file_name)
			l=[]
			for j in range(hh):
				for i in range(ll):
					try:
						if b_grid[j][i][-2]=='1':
							m=[j,i]
							if m not in l:
								l.append([j,i])
								dignoal_continuous_t1(b_grid,j,i,l)
						#print(l)
					except:
						break

			l=dignoal_continuous_cc1(l)
			d={}
			if l==[[]]:
				pass
			else:
				for i in range(len(l)):
					#print(f'    \draw ({l[i][-1][1]},{l[i][-1][0]}) -- ({l[i][0][1]+1},{l[i][0][0]-1});',file=file_name)
					d[l[i][-1][1],l[i][-1][0]]=(l[i][0][1]+1,l[i][0][0]-1)
			#print()
			#print(d)
			j=[]
			for key in d:
				j.append(key)
			#print(j)
			#j=sorted(j,key=lambda x:x[1])
			j=sorted(j,key=itemgetter(1,0))
			#print()
			#print(j)
			for e in j:
				q=d[e]
				print(f'    \draw ({e[0]},{e[1]}) -- ({q[0]},{q[1]});',file=file_name)
				#{e} -- {q};

			print('\\end{tikzpicture}\n'
			      '\\end{center}\n'
			      '\\vspace*{\\fill}\n'
			      '\n'
			      '\\end{document}', file = file_name
			     )
		





frieze=Frieze('frieze_6.txt')
frieze.display()




