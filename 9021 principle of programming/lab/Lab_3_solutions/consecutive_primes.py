# Written by Eric Martin for COMP9021


'''
Finds all sequences of consecutive prime 5-digit numbers, say (a, b, c, d, e, f), such that
b = a + 2, c = b + 4, d = c + 6, e = d + 8, and f = e + 10.
'''


from math import sqrt


def is_prime(n):
    # Only used to test odd numbers.
    return all(n % d for d in range(3, round(sqrt(n)) + 1, 2))


print('The solutions are:\n')
# The list of all even i's such that a + i is one of a, b, c, d, e, f.
good_leaps = tuple(sum(range(0, k, 2)) for k in range(2, 13, 2))
print(good_leaps)
for a in range(10_001, 100_000 - good_leaps[-1], 2):
    # i should be in good_leaps iff a + i is prime for i = 0, 2, 4, ..., 30.
    if all(((i in good_leaps) == is_prime(a + i)) for i in range(0, good_leaps[-1] + 1, 2)):
        for i in good_leaps[: -1]:
            print(a + i, end = '  ')
        print(a + good_leaps[-1])


print('-----')

print(is_prime(13901))
print(is_prime(13902))
if (((i in good_leaps) == True) for i in range(0, good_leaps[-1] + 1, 2)):
	print('!')
else:
	print('?')
	
print('-----')

def p(n):
	for i in range(2,int(sqrt(n)+1)):
		if n==2:
			return True
		if n % i ==0:
			return False
	return True
def p2(n):
    return all([n % d for d in range(3, int(sqrt(n)) + 1)])
n=6
z=[n % d for d in range(3, int(sqrt(n)) + 1)]
print(z)
print(p(6))
print(p2(100))   #这个方法只能判断9以后的数字



