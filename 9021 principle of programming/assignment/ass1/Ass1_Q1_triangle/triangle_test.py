import sys

m=open('/Users/g/desktop/pytest.txt','r')
q=m.readlines()
m.close()
print(q)

l1=[]

for line in q:
	line=line.strip()
	l1.append(line)
print(l1)
numl=len(l1)
l2=[]

for x in range(numl):
	print(l1[x])
	for z in l1[x]:
		l2.append(int(z))
print('aaaaaaaa',l2)
l3=[]
for i in range(0,numl+1):
	l3.append(l2[0:i])
	del l2[0:i]
	print(l2)
	print(l3)
del l3[0]  
print(l3)     
''' 
#---------------
num=len(l3)
print(num)
i=num-2

#倒数第二行 就总共有（最大值）几个[]
record=[]
for r in range(len(l3[-2])):
	record.append([r])
print(record)

while i >=0:
#if i==2:
	num2=len(l3[i])
	#print(num2)
	for j in range(num2):
		print('i:',i,'j:',j)
		cl=l3[i][j]+l3[i+1][j]
		cr=l3[i][j]+l3[i+1][j+1]
		print('cl:',cl,'cr:',cr)
		if cl>cr:
			record[j][0]=[cl]
			record[j].append(l4[i+1][j])
			l3[i][j]=cl
			#record[j].append(l3[i][j])
		elif cr>cl:
			record[j][0]=[cr]
			record[j].append(l4[i+1][j+1])
			l3[i][j]=cr
			#record[j].append(l3[i][j])
		else:
			record[j][0]=[cr]
			record[j].append([l4[i+1][j],l4[i+1][j]])
			l3[i][j]=cl

	i=i-1
print(record)
'''
