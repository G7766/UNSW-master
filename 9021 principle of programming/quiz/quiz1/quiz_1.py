# Written by *** and Eric Martin for COMP9021


'''
Generates a list L of random nonnegative integers at most equal to a given upper bound,
of a given length, all controlled by user input.

Outputs four lists:
- elements_to_keep, consisting of L's smallest element, L's third smallest element,
  L's fifth smallest element, ...
  Hint: use sorted(), list slices, and set()
- L_1, consisting of all members of L which are part of elements_to_keep, preserving
  the original order
- L_2, consisting of the leftmost occurrences of the members of L which are part of
  elements_to_keep, preserving the original order
- L_3, consisting of the LONGEST, and in case there are more than one candidate, the
  LEFTMOST LONGEST sequence of CONSECUTIVE members of L that reduced to a set,
  is a set of integers without gaps.
'''


import sys
from random import seed, randint


try:
    arg_for_seed, upper_bound, length = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, upper_bound, length = int(arg_for_seed), int(upper_bound), int(length)
    if arg_for_seed < 0 or upper_bound < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(0, upper_bound) for _ in range(length)]
print('\nThe generated list L is:')
print('  ', L)

l=list(L)
print(l)
L=list(set(L))
print(L)
L.sort()
print(L)
L_1 = []
L_2 = []
L_3 = []
elements_to_keep=[]

#elements_to_keep
k=len(L)
print(k)
i=0
while i < k:
  elements_to_keep.append(L[i])
  i=i+2
print(elements_to_keep)
#L_1
k1=len(elements_to_keep)
for i in range(length):
  for q in range(k1):
    if l[i]==elements_to_keep[q]:
      L_1.append(l[i])
print(L_1)
#L_2
ll=list(L_1)
L_2=list(set(ll))
L_2.sort(key=L_1.index)


#L_3
lon=[]
print(length)
for i in range(length):
  for q in range(i+1,length+1):
    lll=l[i:q]
    lll.sort()
    lll_set=list(lll)
    count=0
    print(lll_set)
    print(i,q)
    for n in range(q-i):
      if n==0:
        pass
      elif n!=0:
        if lll_set[n]-lll_set[n-1]==1 or lll_set[n]-lll_set[n-1]==0:
          count=count+1
        else:
          count=0
          break
    print(count)
    lon.append(count)
print(lon)
lon=sorted(set(lon))
lon=lon[::-1]
print(lon)



#again    find count == lon[0]  i and q
www=[] 
for i in range(length):
  for q in range(i+1,length+1):
    lll=l[i:q]
    lll.sort()
    lll_set=list(lll)
    count=0
    for n in range(q-i):
      if n==0:
        pass
      elif n!=0:
        if lll_set[n]-lll_set[n-1]==1 or lll_set[n]-lll_set[n-1]==0:
          count=count+1
        else:
          count=0
          break
    if count==lon[0]:
      print(lon[0])
      print(i,q)
      f=i
      j=q
      www.append(l[i:q])
      break
L_3=www[0]
#L_3=l[f:j]
print(L_3)






# Replace this comment with your code
    
print('\nThe elements to keep in L_1 and L_2 are:')
print('  ', elements_to_keep)
print('\nHere is L_1:')
print('  ', L_1)
print('\nHere is L_2:')
print('  ', L_2)
print('\nHere is L_3:')
print('  ', L_3)


