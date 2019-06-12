#-------------------------------------------------------------------------(1)
#交集，并集，差集
q={1,2}
print(len(q))
z={2,3,5}
p=q.union(z)
print(p)
#union
#union = b.extend([v for v in a])
d={1,2,3,4}
g=q.intersection(d)
print(g)
#intersection
#intersection=[v for v in a if v in b]
gg=q.difference(d)
print(gg)
ggg=d.difference(q)
print(ggg)
#difference
#difference= [v for v in a if v not in b]

l = list(set(q).intersection(set(z)))
print(l)
#-------------------------------------------------------------------------(2)
music_media = ['compact disc', '8-track tape', 'long playing record']
new_media = ['DVD Audio disc', 'Super Audio CD']
music_media.append([v for v in new_media])
print(music_media)
#使用append的时候，是将new_media看作一个对象，整体打包添加到music_media对象中。
music_media = ['compact disc', '8-track tape', 'long playing record']
new_media = ['DVD Audio disc', 'Super Audio CD']
music_media.extend([v for v in new_media])
print(music_media)
#使用extend的时候，是将new_media看作一个序列，将这个序列和music_media序列合并，并放在其后面。

#-------------------------------------------------------------------------(3)

s={1,2,3}
q=312
p=set(int(i) for i in str(q))
if p==s:
    print('true')
else:
    print('f')

m={3,2,1}
print(s==m)
#-------------------------------------------------------------------------(4)
from random import seed, randint ,randrange
import sys
#grid
def display_grid():
    for i in range(len(grid)):
        print('   ', ' '.join(str(int(grid[i][j] != 0)) for j in range(len(grid))))
'''
try:
    arg_for_seed, density, dim = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, density, dim = int(arg_for_seed), int(density), int(dim)
    if arg_for_seed < 0 or density < 0 or dim < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
'''
arg_for_seed=2
density=4
dim=10
seed(arg_for_seed)
grid = [[randint(0, density) for _ in range(dim)] for _ in range(dim)]
print(grid)
print('Here is the grid that has been generated:')
display_grid()

#旋转堆成
#是旋转加对折
def rotation90(z):
	for i in range(len(z)):
		for j in range(i,len(z)):
			temp=z[i][j]
			z[i][j]=z[j][i]
			z[j][i]=temp
	return z


#-------------------------------------------------------------------------(5)
#list
list1=[1,2,3]
list1.append(4)
print(list1)

list2=[]
list2.extend([list1[0],list1[2]])
print(list2)
#注意：extend与append的区别就是extend可以同时添加多个元素

#insert
list1.insert(3,'x')
print(list1)
#+
list3=[2,3,1]
list4=['a','b']
list5=list3+list4
print(list5)

#list删除元素
li=[1,2,3,4,5,6]
# 1.使用del删除对应下标的元素
del li[2]
print(li)

#2.使用.pop()删除最后一个元素
li.pop()
print(li)
# 3.删除指定值的元素
li.remove(4)
print(li)
# 4.使用切片来删除
li=li[:-1]
print(li)
# !!!切忌使用这个方法，如果li被作为参数传入函数，
# 那么在函数内使用这种删除方法，将不会改变原list

ll=[1,2,3,4,5,6]
print(ll[:3])
print(ll[:6:2])
print(ll[::-1])
q=reversed(ll)
print(q)

aList = [123, 'xyz', 'zara', 'abc']
print(aList.index('xyz'))
#-------------------------------------------------------------------------(6)
dict1= {'Alice': '2341', 'Beth': '9102', 'Cecil': '3258'}
print(len(dict1))
for key in dict1.keys():
	print(key)
for value in dict1.values():
	print(value)
print(dict1['Alice'])
dict1['aaa']=123
print(dict1)
del dict1['aaa']
print(dict1)
dict1.clear()
print(dict1)
del dict1
#print(dict1)   不存在了

#-------------------------------------------------------------------------(7)
import copy
ll=[1,2,3,4]
lll=copy.deepcopy(ll)
print(lll)

#-------------------------------------------------------------------------(8)
from math import gcd,sqrt
#-------------------------------------------------------------------------(9)
'''
import os
for filename in os.listdir(directory):
  name_gender_count_list=[]
  male_list=[]
  female_list=[]
  count_male_list=[]
  count_female_list=[]
  if not filename.endswith('.txt'):   #filename!='yob1880.txt'filename.endswith('.txt')
    continue
  else:
  	#print(filename)
  	with open(directory+'/'+filename) as data_file:
  		for line in data_file:
  			line=line.strip('\n')
  			name,gender,count=line.split(',')
  			if gender=='M':
  				male_list.append([name,int(count)])
  				count_male_list.append(int(count))
  			else:
  				female_list.append([name,int(count)])
  				count_female_list.append(int(count))


if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()
'''

q=[1,2,3]
print('?',all(q))


#-------------------final exam study

from statistics import mean, median, pstdev
L=[-20, 25, 19, -34, -3, 27, 10, 30, 24, -42]
print(f'The mean is {mean(L):.2f}.')   #平均数
print(f'The median is {median(L):.2f}.')     #中位数
print(f'The standard deviation is {pstdev(L):.2f}.')  #方差

from math import factorial
the_input=15
print(factorial(the_input))  #算 15！阶乘



d={1:2,2:3}
for value in d:
    print(value)
    print(d[value])

