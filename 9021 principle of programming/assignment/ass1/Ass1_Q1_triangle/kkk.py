l3=[[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
l4=[[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
l_test=[[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 6]]
#l3=[[1],[2,2],[1,2,1],[2,1,1,2],[1,2,1,2,1],[2,1,2,2,1,2]]
#l4=[[1],[2,2],[1,2,1],[2,1,1,2],[1,2,1,2,1],[2,1,2,2,1,2]]


num=len(l3)
print(num)
i=num-2

#倒数第二行 就总共有（最大值）几个[]
record=[]

for r in range(len(l3[-2])):
	record.append([r])
print(record)

record_a=[]
for r in l3[-1]:
	record_a.append([r,[r],1])
print(record_a)

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
#找到record里最长的纪录
length_list=[]
for q in record:
	print(q)
	length_list.append(len(q))
print(length_list)
max_len=max(length_list)




























