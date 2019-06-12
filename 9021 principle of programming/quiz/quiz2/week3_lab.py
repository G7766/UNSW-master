
23/66
L=['1','2','6','1','7']
''.join(str(e) for e in L)




'**'.join(str(e) for e in L)



f={2:3,4:1,6:9,3:0,19:8}
#f.key()
for d in f:
    print(d)

sorted(f)


{f[d] for d in f}


m={2:[2,5],3:[2,11],4:[5]}
for q in m:
    print(m[q])

qq=set()
for q in m:
    print(m[q])
    qq|= set(m[q])
print(qq)



{e for q in m for e in m[q]}

from cllections import defaultdict
def m(n):
    #f={}
    f=defaultdict(int)
    #D[3]+=4
    #f=defaultdict(list)
    #D[3]+=[3,4]
    
    d=2
    while n !=1:
        if n%d==0:
            f[d]=1
            n//=d
            while n%d==0:
                f[d]+=1
                n//=d
        d+=1
    return f
        