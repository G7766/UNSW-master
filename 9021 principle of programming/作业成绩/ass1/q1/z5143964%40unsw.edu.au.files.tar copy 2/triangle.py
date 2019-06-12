# Written by Guan PeiGuo for COMP9021


# Insert your code here

# Written by Guan PeiGuo for COMP9021
import sys
import copy

a=input('Enter the file name you want to open: ')
#a='/Users/g/desktop/pytest.txt'

try:
    f=open(a,'r')
    q=f.readlines()
    #print(q)
    if q==[]:
    	raise ValueError
    	sys.exit()
except IOError:
    print('The file is not exist.')
    sys.exit()
except ValueError:
	print('Incorrect input, giving up!')
	sys.exit()
finally:
	f.close()

# Insert your code here


#print(f.read())

#-------------------------------------------change_file_to_list

l1=[]

for line in q:
	line=line.strip()
	l1.append(line)
#print(l1)
num1=len(l1)
l2=[]

for x in range(num1):
	#print(l1[x])
	for z in l1[x]:
		#print(z)
		if z==' ':
			pass
		else:
			l2.append(int(z))
#print(l2)

l3=[]
for i in range(0,num1+1):
	l3.append(l2[0:i])
	del l2[0:i]
	#print(l2)
	#print(l3)
del l3[0]        
#print(l3)
#----------------------------------------------calculate




#print('l3:',l3)
l4=copy.deepcopy(l3)
num=len(l3)
#print(num)
i=num-2


record_a=[]
for r in range(len(l3)+1):
	record_a.append([r])
#print(record_a)

for r in l3[-1]:
	n=len(l3[-1])
	record_a[n].append([r,[r],1])
#print(record_a)
for r in range(len(record_a)):
	record_a[r].pop(0)
#print('record_a:',record_a)


while i >=0:
#if i==3:
	num2=len(l3[i])
	#print('num2:',num2)
	record_b=list(record_a)
	record_c=record_a[num2+1]
	#print(record_b)
	#print('record_c:',record_c)

	for j in range(num2):
		#print('i:',i,'j:',j)
		cl=l3[i][j]+l3[i+1][j]
		cr=l3[i][j]+l3[i+1][j+1]
		#print('cl:',cl,'cr:',cr)

		if cl>cr:
			l3[i][j]=cl
			q=copy.deepcopy(record_c[j])
			q[0]=cl
			q[1].append(l4[i][j])
			#print('qaaa:',q)
			record_b[i+1].append(q)
			#print('record_b:',record_b)
	
		elif cr>cl:
			l3[i][j]=cr
			q=copy.deepcopy(record_c[j+1])
			#print('q???:',q)
			q[0]=cr
			q[1].append(l4[i][j])
			record_b[i+1].append(q)
			#print('q!!!!:',q)
			#print('record_b:~~~~~~~~`',record_b)
			#print('record_c:~~~~~~~~`',record_c)


#相等的时候，只要把左边的那个数放进去，得到的tree就是最左边的！！！！！


		else:
			l3[i][j]=cl
			q=copy.deepcopy(record_c[j])
			q[0]=cl
			q[1].append(l4[i][j])
			q[2]=record_a[i+2][j][2]+record_a[i+2][j+1][2]
			record_b[i+1].append(q)



	#print('record_b:',record_b)
	i=i-1

final_list=record_b[1]

#print('final_record_b:',final_list)

largest_sum=final_list[0][0]
path=final_list[0][2]
leftmost=final_list[0][1]
leftmost.reverse()
print('Which data file do you want to use?',a)
print('The largest sum is:',largest_sum)
print('The number of paths yielding this sum is:',path)
print('The leftmost path yielding this sum is:',leftmost)












