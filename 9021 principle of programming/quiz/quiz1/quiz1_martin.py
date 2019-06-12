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






def determine_elements_to_keep(L):
  '''
  >>> determine_elements_to_keep([])
  []
  >>> determine_elements_to_keep([0])
  [0]
  >>> determine_elements_to_keep([0,0])
  [0]
  >>> determine_elements_to_keep([0,1])
  [0]
  >>> determine_elements_to_keep([1,0])
  [0]
  >>> determine_elements_to_keep([1,0,0])
  [0]
  >>> determine_elements_to_keep([0,1,0])
  [0]
  >>> determine_elements_to_keep([0,0,1])
  [0]
  >>> determine_elements_to_keep([0,1,2])
  [0,2]
  >>> determine_elements_to_keep([1,2,0])
  [0,2]
  '''
  elements_to_keep=[]
  if len(L)==1:
    elements_to_keep=L
  return elements_to_keep

def determine_L_1(L):
  
  L_1=[]
  return L_1

def determine_L_2(L):
  L_2=[]
  return L_2

def determine_L_3(L):

  '''
  >>> determine_L_3([0])
  []
  >>> determine_L_3([0])
  [0]
  >>> determine_L_3([0,0])
  [0,0]
  >>> determine_L_3([0,1])
  [0,1]
  >>> determine_L_3([1,0])
  [1,0]
  >>> determine_L_3([0,2])
  [0]
  >>> determine_L_3([2,0])
  [2]
  >>> determine_L_3([0,0,0])
  [0,0,0]
  >>> determine_L_3([0,1,4])
  [0,1]
  >>> determine_L_3([1,0,4])
  [1,0]
  >>> determine_L_3([0,4,5])
  [4,5]
  >>> determine_L_3([0,2,4])
  [0]
  '''
  L_3=[]
  return L_3



if __name__=='__main__':
  import doctest
  doctest.testmod()


L=[2,1,4,8,6,9,0,10]
l=sorted(L)
#L_1
L_1=l[::2]
#L.sort()
print(L)
print(l)
print(L_1)


#L_2
i=0
output=[]
while i< len(L):
    if L[i]%2:
        output.append(L[i])
    i+=1
print(output)
L_2=output
print(L_2)
#output=[e for e in L if e % 2]
#def is_odd(n):
    return n % 2==1
#list(filter(is_odd,L))
#list(filter(lambda x: x%2==1,L))



#L_3

# Replace this comment with your code
    
print('\nThe elements to keep in L_1 and L_2 are:')
print('  ', elements_to_keep)
print('\nHere is L_1:')
print('  ', L_1)
print('\nHere is L_2:')
print('  ', L_2)
print('\nHere is L_3:')
print('  ', L_3)


