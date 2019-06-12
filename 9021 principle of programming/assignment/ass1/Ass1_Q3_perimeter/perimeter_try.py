
l=[[-15,0,5,10],[-5,8,20,25],[15,-4,24,14],[0,-6,16,4],[2,15,10,22],[30,10,36,20],[34,0,40,16]]
l.sort()
print(l)


vertical=list(l)
print('vertical:',vertical)

horizon=[]
for i in l:
	horizon.append([i[1],i[0],i[3],i[2]])
horizon.sort()
print('horizon:',horizon)

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
			print('i',i)
			for j in list:
				#print('for',j)
				if j[0]<x<j[2] and j[1]<=y<j[3]:
					print(j[1],j[3])
					y=y+1
					print(x,y)
					break
				elif j==list[-1]:
					y=y+1
					size=size+1
					print('size:',size)

	return size
'''
q=calculate(horizon)
print(q)
'''
p=calculate(vertical)
print(p)
print(p)
'''
pre=2*q+2*p
print(pre)
'''









