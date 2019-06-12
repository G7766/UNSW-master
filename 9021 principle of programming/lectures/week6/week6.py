def add_1(L):
    if not L:
        return 0
    return add_1(L[:-1])+L[-1]

print(add_1([1,5,6,10]))

def add_2(L):
    if not L:
        return 0
    return add_2(L[1:])+L[0]

print(add_2([1,5,6,10]))

def add_3(L):
    if not L:
        return 0
    if len(L)==1:
        return L[0]
    return add_3(L[:len(L)//2])+add_3(L[len(L)//2:])

print(add_3([1,5,6,10]))


#0 1 1 2 3 5
def fibo(n):
    if n<=1:
        return n
    return fibo(n-1) + fibo(n-2)
print(fibo(20))


def fibo_1(n):
    if n<=1:
        return n
    previous,current=0,1
    for _ in range(2,n+1):
        previous,current=current,previous+current        
    return current
print(fibo_1(20))

def fibo_2(n,fibonacci={0:0,1:1}):
    if n not in fibonacci:
        fibonacci[n]=fibo_2(n-1)+fibo_2(n-2)
        #fibonacci[n]=fibo_2(n-1)+fibonacci[n-2]  is ok as well
    #print(fibonacci)
    return fibonacci[n]
print(fibo_2(20))



def hanoi(n,A,B,C):
    if n ==1:
        print(f'Move disk from {A} to {C}')
    else:
        hanoi(n-1,A,C,B)
        print(f'Move disk from {A} to {C}')
        hanoi(n-1,B,A,C)
print(hanoi(1,'A','B','C'))      
print(hanoi(2,'A','B','C')) 

n=10
s=list(range(n,0,-1)),[],[]
print(s)
q=[]
for i in range(n):
    q.append(2**n-1)
print(q)


def f():
    print('A')
    yield 2
    print('B')
    yield 3
    print('C')
    yield 4
    print('D')
    yield 5
x=f()
next(x)
next(x)
next(x)
next(x)
for i in x:
    print(i)
#next(x)


z=[1,2,3,4]
print(z[:-1])


def permute(L):
    if len(L)<=1:
        yield L
    else:
        for i in range(len(L)):
            L[0],L[i]=L[i],L[0]
            for L1 in permute(L[1:]):
                yield [L[0]]+L1

permute([])

for L in permute([]):
    print(L)
                
for L in permute([1,2]):
    print(L)
for L in permute([1,2,3]):
    print(L)



def convert_to_binary(N):
    if N <=1:
        print(N,end='')
    else:
        convert_to_binary(N//2)
        #print('?:',N%2)
        print(N%2,end='')

print(convert_to_binary(23))
