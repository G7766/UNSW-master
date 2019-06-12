# Written by Guan PeiGuo for COMP9021


# Insert your code here
import sys
a=input('Which data file do you want to use?')
#d='/Users/g/desktop/'
l=[]
try:
	#with open(d+a,'r') as file:
	with open(a,'r') as file:
		for line in file:
			line=line.strip()
			line=line.split()
			ll=[]
			for i in line:
				ll.append(int(i))
			#print(ll)
			l.append(ll)
		#print('l:',l)
except ValueError:
	print('Incorrect Input, giving up!')
	sys.exit()
except IOError:
	print('Incorrect Input, giving up!')
	sys.exit()


#-------------cal
l.sort()
#print(l)


vertical=list(l)
#print('vertical:',vertical)

horizon=[]
for i in l:
	horizon.append([i[1],i[0],i[3],i[2]])
horizon.sort()
#print('horizon:',horizon)

'''

#水平

horizon_size=[]
for x in l:
	horizon_size.append([x[0],x[2]])
print(horizon_size)

vertical_size=[]
for x in l:
	vertical_size.append([x[1],x[3]])
print()
'''
def calculate(list):
	size=0
	for i in list:
		x=i[0]
		y=i[1]
		while y<i[3]:
			for j in list:
				#print('for',j)
				if j[0]<x<j[2] and j[1]<=y<j[3]:
					y=y+1
					#print(y)
					break
				elif j==list[-1]:
					y=y+1
					size=size+1
	return size
#horizon
q=calculate(horizon)
#print(q)
#vertical
p=calculate(vertical)
#print(p)

pre=2*q+2*p
print('The perimeter is:',pre)
