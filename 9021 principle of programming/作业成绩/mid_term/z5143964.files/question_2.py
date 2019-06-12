import sys
from math import factorial


def f(n):
    '''
    >>> f(0)
    0! is 1
    There is no 3 in 1
    >>> f(10)
    10! is 3628800
    There is one 3 in 3628800
    >>> f(20)
    20! is 2432902008176640000
    There is one 3 in 2432902008176640000
    >>> f(24)
    24! is 620448401733239439360000
    There are 5 3's in 620448401733239439360000
    >>> f(28)
    28! is 304888344611713860501504000000
    There are 3 3's in 304888344611713860501504000000
    >>> f(3); f(11); f(15)
    3! is 6
    There is no 3 in 6
    11! is 39916800
    There is one 3 in 39916800
    15! is 1307674368000
    There are 2 3's in 1307674368000
    '''
    if n < 0:
        sys.exit()
    n_factorial = factorial(n)
    nb_of_threes = 0
    # Insert your code here
    l=[]
    q=str(n_factorial)
    x=len(q)
    for i in range(x):
        l.append(q[i])
    #print(l)
    qq=str(x)
    nn=len(qq)
    #print(qq)
    count=0
    ll=[]
    for i in range(len(qq)):
        ll.append(qq[i])
    for j in range(len(l)):
        if l[j]=='3':
            count=count+1
    #print('count:',count)
    if count==0:
        print(f'{n}! is {n_factorial}')
        print(f'There is no 3 in {n_factorial}')
    elif count==1:
        print(f'{n}! is {n_factorial}')
        print(f'There is one 3 in {n_factorial}')
    else:
        print(f'{n}! is {n_factorial}')
        print(f'There are {count} 3\'s in {n_factorial}')
        

                
        
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
