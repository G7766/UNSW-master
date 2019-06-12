'''
from math import sqrt

def is_prime(n):
	for d in range(2,int(sqrt(n))+1):
		if not n%d:         #if n%d is None:
			return False
	return True


if __name__=='__main__':
	import doctest
	doctest.testmod()

print(is_prime(2))

def generate_all_prome_up_to(n):
    sieve=[True]*(n+1)
    print(sieve)
generate_all_prome_up_to(7)


from math import sqrt
def generate_all_primes_up_to(n):
    sieve=[True]*(n+1)
    for i in range(2,round(sqrt(n))+1):
        d=i**2
        while d<=n:
            sieve[d]=False
            d+=i
    for i in range(2,n+1):
        if sieve[i]:
            print(i)
generate_all_primes_up_to(100)




from math import sqrt
def generate_all_primes_up_to(n):
    list_of_primes=list(range(2,n+1))
    i = 0
    while list_of_primes(i)<=(round(sqrt(n))+1):
        k=0
        while True:
            factor=list_of_primes(i) * list_of_primes(i+k)
            if factor> n:
                break
            while factor <= n:
                list_of_primes.remove(factor)
                factor*=list_of_primes(i)
            k+=1
        i+=1

#help(zip) 
zip((1000,3),(2000,4),(3000,5),(4000,6))    
z=list(zip((1000,3),(2000,4),(3000,5),(4000,6)))
print(z)

'''
'''
x=31456
print(str(x))
print(set(str(x)))
print(len(set(str(x)))!=len(str(x)))
y=51278
print(len(set(str(y)))!=len(str(y)))
x=467
str(x)
digits_seen={'0','2','5'}
q=set(str(x))|digits_seen
print(q)
print(len(set(str(x))))
print(len(digits_seen))

'''

x=3145

digits_in_x=set()
while x:
	digits_in_x.add(x%10)
	x //= 10
print('---')
print(digits_in_x)
print('----')
x={1,3}
y={3,4,5}
z=x|y
print(z)


print(bin(645))

print(bin(1<<5))        #把1 向左移动五

print('---------')
print(bin(35))
print(bin(46))
print(bin(35 & 46))      # & (and):  1 1 =1 ，1 0 = 0 ， 0 0 = 0

print(bin(35 |46 ))		# |(or)):  1 1= 1 , 1 0= 1, 0 0=0 

