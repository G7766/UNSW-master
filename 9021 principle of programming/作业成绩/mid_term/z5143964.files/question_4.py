import sys
from math import sqrt

def prime(n):
    if n==2:
        return 0
    if n==3:
        return 0
    mm=int(n/2+1)
    ll=[i for i in range(2,mm+1)]
    #print(ll)
    for j in ll:
        if n%j==0:
            a=1
            break
        else:
            a=0
    return a
    
def f(n):
    '''
    Won't be tested for n greater than 10_000_000
    
    >>> f(3)
    The largest prime strictly smaller than 3 is 2.
    >>> f(10)
    The largest prime strictly smaller than 10 is 7.
    >>> f(20)
    The largest prime strictly smaller than 20 is 19.
    >>> f(210)
    The largest prime strictly smaller than 210 is 199.
    >>> f(1318)
    The largest prime strictly smaller than 1318 is 1307.
    '''
    if n <= 2:
        sys.exit()
    largest_prime_strictly_smaller_than_n = 0
    # Insert your code here
    for i in reversed(range(n)):
        q=prime(i)
        if q==1:
            continue
        else:
            largest_prime_strictly_smaller_than_n=i
            break
        
    print(f'The largest prime strictly smaller than {n} is {largest_prime_strictly_smaller_than_n}.')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
