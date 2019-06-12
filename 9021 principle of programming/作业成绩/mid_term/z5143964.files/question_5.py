

def f(word):
    '''
    Recall that if c is an ascii character then ord(c) returns its ascii code.
    Will be tested on nonempty strings of lowercase letters only.

    >>> f('x')
    The longest substring of consecutive letters has a length of 1.
    The leftmost such substring is x.
    >>> f('xy')
    The longest substring of consecutive letters has a length of 2.
    The leftmost such substring is xy.
    >>> f('ababcuvwaba')
    The longest substring of consecutive letters has a length of 3.
    The leftmost such substring is abc.
    >>> f('abbcedffghiefghiaaabbcdefgg')
    The longest substring of consecutive letters has a length of 6.
    The leftmost such substring is bcdefg.
    >>> f('abcabccdefcdefghacdef')
    The longest substring of consecutive letters has a length of 6.
    The leftmost such substring is cdefgh.
    '''
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
    rr=[]
    count=1
    for i in range(n2):
        for j in range(i,n2):
            for z in range(n1):
                if ll[i:j]==l[z:z+j-i]:
                    r.append(j-i)
                    rr.append(ll[i:j])
                    desired_substring=ll[i:j]
                
    desired_length=max(r)
    #desired_substring
        

    print(f'The longest substring of consecutive letters has a length of {desired_length}.')
    print(f'The leftmost such substring is {desired_substring}.')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
