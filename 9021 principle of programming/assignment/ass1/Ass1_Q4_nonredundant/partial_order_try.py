from collections import defaultdict
import copy
import sys


a=input('file:')
d='/Users/g/Desktop/'

try:
	with open(d+a,'r') as file:
		l=[]
		for line in file:
			line=line.strip()
			print(line)
			line=line.split()
			print(line)
			for i in line:
				l.append([int(i[2]),int(i[4])])
			print(l)
		print('l:',l)			
except ValueError:
	print('Incorrect input, giving up!')
	sys.exit()
except IOError:
	print('Incorrect input, giving up!')
	sys.exit()
#l=[[3,5],[4,2],[5,2],[2,1],[3,1],[4,1]]
#l1=[[3,5],[5,2],[2,6],[2,1],[3,6],[6,1],[4,2],[4,1]]
#l=[[1,2],[2,3],[3,4],[1,3],[2,4]]
'''
ancestor={}
destant=[]
for i in l:
	if str(i[0]) in ancestor:
		#print(str(i[0]))
		ancestor[str(i[0])].append(i[1])
	else:
		#print(str(i[0]))
		ancestor[str(i[0])]=[i[1]]
print(ancestor)
'''

ll=copy.deepcopy(l)
#lll=copy.deepcopy(l)
record=[]
count=1
size=len(l)
while count!=size+1:
	for a in l:
		for b in ll:
			if a==b:
				continue
			elif a[1]==b[0]:
				if [a[0],b[1]] in record:
					continue
				else:
					record.append([a[0],b[1]])
			elif a[1]!=b[0]:
				pass
	for i in ll:
		for j in record:
			if j==i:
				ll.remove(i)
	#print('record:',record)
	#print('ll:',ll,'\n')
	l=record
	count=count+1

print(ll)
print(record)








