
import sys
from random import seed, randint


dim = 10
grid = [[None] * dim for _ in range(dim)]
print(grid)
for i in range(dim):
    print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))

density=9

for i in range(dim):
    for j in range(dim):
        grid[i][j] = int(randint(0, density) != 0)
print(grid)
for i in range(dim):
    print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))
#print('l:',grid)


dim = 10
#grid=[[1, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 1, 1, 1, 1], [0, 1, 1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
#print(grid)
for i in range(dim):
    print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(dim)))

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
print('path:',path)	
print(record)
print(len(record))

m=4
for i in record:
	a=i[0]
	b=i[1]
	l[a][b]=m
print(l)
for i in range(dim):
    print('   ', ' '.join(str(int(l[i][j])) for j in range(dim)))
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
print(ll)

	
for i in range(length):
	for j in range(length):
		record_1=[[i,j]]
		q=1
		cal_2(i,j,l)
		ll[i][j]=q
		q=0

print(ll)

lll=[]
for m in ll:
	lll.append(max(m))
print(lll)
print(max(lll))





