
def f(word):
    desired_length = 0
    desired_substring = ''
    # Insert your code here
    l=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    ll=[]
    for x in word:
        ll.append(x)
    n1=len(l)
    n2=len(ll)
    #print(ll)
    r=[]
    count=1
    for i in range(n2):
        for j in range(i,n2):
            for z in range(n1):
                if ll[i:j]==l[z:z+j-i]:
                    r.append(j-i)
                
    desired_substring=max(r)  

    print(f'The longest substring of consecutive letters has a length of {desired_length}.')
    print(f'The leftmost such substring is {desired_substring}.')
f('xy')
if __name__ == '__main__':
    import doctest
    doctest.testmod()
