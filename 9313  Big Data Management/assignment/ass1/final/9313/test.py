line = 'ni hao wo shi shui'

z = line.split(" ")
print(z)

for i in range(len(z)-1):
	m=''
	for j in range(2):
		m = m + z[i+j] + ' '
	print(m)

import numpy as np
z= [1,2,3,4,5]
l=np.array(z)[:-1]

print(l)

q = "apache hadoop is a collection of open-source software utilities that facilitate using a network of many computers to solve problems involving massive amounts of data and computation."

l = q.split(' ')
print(l)
print(len(l))