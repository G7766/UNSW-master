import sys
from math import gcd


try:
    numerator, denominator = input('Enter two strictly positive integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    numerator, denominator = int(numerator), int(denominator)
    if numerator <= 0 or denominator <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')






from math import sqrt

def gcd(n,m):
    while m:
        #print(n,m)
        n,m=m,n%m
    #print(n,m)
    q=abs(n-m)
    return q

def if_is_finite(a):
    while a:
        if a%2==0:
            a=a/2
        elif a%5==0:
            a=a/5
        else:
            #print(a)
            return a
def the_integral_part(n,m):
    return n//m
    

'''
def is_prime(n):
    for d in range(2,int(sqrt(n)+1)):
        if not n%d:
            return False
    return True

def if_is_finite(n,m):
    if m%2==0 or m%5==0 :
        print('finite expansion')
        return 1
    elif n%m==0:
        print('finite expansion')
        return 1
    else:
        print('infinite expansion')
        return 0

'''

def decimal2str(d):
    l=list(str(d))
    del l[0:2]
    l1=l
    num=len(l1)
    l2=''
    for i in l1:
        l2=l2+i
    return l2



def the_decimal_part(d):
    l=list(d)
    #print(l)
    num=len(l)
    #print(num)
    del l[0:2]
    l2=l
    #print(l2)


    num1=len(l2)
    #print(num1)

    exit_lag=False
    tau=0

    for i in range(num1):
        w=0
        for q in range(i+1,num1):
            c=q-i
            if l2[i:q]==l2[q:q+c] and l2[i+1:q+1]==l2[q+1:q+c+1]:
                tau=l2[i:q]
                print('??:',tau)
                pos=i
                count=c
                print(c)
                #print(tau,count)
                if tau==['0']*c:
                    continue
                else:
                    exit_lag=True
                    break

        if exit_lag==True:
            break
    
    tau1=''
    sig=''
    if tau==0:
        tau1=tau
        for q in l2:
            sig=sig+q
    else:
        for i in tau:
            tau1=tau1+i
        #print('tau:',tau1)
        if pos==0:
            sig=0
        else:
            for i in range(pos):
                sig=sig+l2[i]


    #print('tau:',tau1,'sig:',sig)
    return tau1,sig




#--------------------------





gd=gcd(numerator,denominator)
#print(gd)
num,denom=numerator//gd,denominator//gd
#print(numerator,denominator)

if denom==1:

    has_finite_expansion=True
    
    integral_part=num
    print('integral_part is:',integral_part)
    sigma=0
    tau=0
    if sigma==0:
            sigma=''
    print('sigma is:',sigma)
    print('tau is:',tau)
    #print('it has finite ex11111')
    
    
else:
    a=if_is_finite(denom)
    if a==1:
        
        has_finite_expansion=True
        
        #print('finite exp222')
        j=num/denom
        integral_part=the_integral_part(num,denom)
        #print('integral_part is:',integral_part)
        jd=j-integral_part
        tau=0

        sigma=decimal2str(jd)
        if sigma==0:
            sigma=''
        #print('sigma is:',jd,'tau is:',tau)
        
        
    else:

        has_finite_expansion=False
        
        #print('definite exp')
    
        j=num/denom
        #print(j)
        integral_part=the_integral_part(numerator,denominator)
        #print('integral_part is:',integral_part)
        #decimal:
        jd=j-integral_part
        #decimal_part=[]
        nn=('%.20f' %jd)
        x,y=the_decimal_part(nn)
        tau=x
        if tau==0:
            has_finite_expansion=True
        sigma=y
        if sigma==0:
            sigma=''
        print('sigma is:',sigma,'tau is:',tau)




if has_finite_expansion:
    print(f'\n{numerator} / {denominator} has a finite expansion')
else:
    print(f'\n{numerator} / {denominator} has no finite expansion')
if not tau:
    if not sigma:
        print(f'{numerator} / {denominator} = {integral_part}')
    else:
        print(f'{numerator} / {denominator} = {integral_part}.{sigma}')
else:
    print(f'{numerator} / {denominator} = {integral_part}.{sigma}({tau})*')











