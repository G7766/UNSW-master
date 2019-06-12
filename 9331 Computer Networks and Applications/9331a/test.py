import random
import time
#with open("test1.txt",'r') as f:
#	data = f.read()

#print(data)
import hashlib

'''
if __name__ == '__main__':
	seed = '100'
	a=int(seed)
	random.seed(a)
	print(random.random())
	print(random.random())
	print(random.random())
	print(random.random())
	print(random.random())
	print(random.random())
	print(random.random())
'''
import datetime
nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
k = time.time()
print(k)
print(nowTime)
print(nowTime[-2:])
print(k)
k = k + 1000/1000
print(k)

print(50/8)

file = 'test.py'
with open(file,'rb') as f:
	z = f.read()
q1=z
q2=z
print(z)
print()
print('-------------------------')
print(z)
print('-------------------------')
print(type(z))
l = str(z)
print(l)
print(type(l))
l = list(l)

print('-------------------------')
print()
def get_token(payload):
    md5str = payload.decode()
  #生成一个md5对象
    m1 = hashlib.md5()
  #使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token


a = get_token(z)
print(a)
q=list(a)
print(q)
if q[1]=='1':
	q[1]='0'
else:
	q[1]='1'
print(q)

l = ''.join(q)
print(l)




q1= get_token(q1)
q2= get_token(q2)


print(q1)
print(q2)


z= [1,2,3,4,5]
print(z[:-1])

from collections import Counter
q = [1,1,3,4,5,6,5]
z = Counter(q)
print(z)
k = 0
for i in z:
	if z[i] > 1:
		k= k + 1
print(k)

import pickle
k = 'asdasdada'
kk = pickle.dumps(k)
a = list(kk)


print(a)
print(kk)
a[2]=1

zz = bytes(a)
print(zz)

file = 'test0.pdf'
with open(file,'rb') as f:
	data = f.read()

print(data)

l = k.encode()
print(l)

lll = bytearray(l)
lll[0]=1
print(lll)
z =bytes(lll)
print(z)


a= 'sdawdwq'
z = k.encode()
zz = a.encode()
print(z)
print(zz)
l = z +zz 
print(l)



print(l.decode())




