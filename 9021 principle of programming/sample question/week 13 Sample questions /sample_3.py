'''
Given a word w, a good subsequence of w is defined as a word w' such that
- all letters in w' are different;
- w' is obtained from w by deleting some letters in w.

Returns the list of all good subsequences, without duplicates, in lexicographic order
(recall that the sorted() function sorts strings in lexicographic order).

The number of good sequences grows exponentially in the number of distinct letters in w,
so the function will be tested only for cases where the latter is not too large.

'''
from operator import itemgetter, attrgetter

def good_subsequences(word):
    '''
    >>> good_subsequences('')
    ['']
    >>> good_subsequences('aaa')
    ['', 'a']
    >>> good_subsequences('aaabbb')
    ['', 'a', 'ab', 'b']
    >>> good_subsequences('aaabbc')
    ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
    >>> good_subsequences('aaabbaaa')
    ['', 'a', 'ab', 'b', 'ba']
    >>> good_subsequences('abbbcaaabccc')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb']
    >>> good_subsequences('abbbcaaabcccaaa')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    >>> good_subsequences('abbbcaaabcccaaabbbbbccab')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    '''
    # Insert your code here
    if word=='':
        return ['']
    k=word[0]
    b=[word[0]]
    #print(word)
    for i in range(len(word)-1):
        if i==len(word)-1:
            break
        if word[i]==word[i+1]:
            continue
        else:
            b.append(word[i+1])
    #print(b)
    k=0
    c=['']
    for i in range(len(b)):
        if b[i] in c:
            continue
        else:
            c.append(b[i])
            f(b[i],i,b,c)
    #print(c)
    #c.sort()
    #print(c)
    c=sorted(c, key=str.lower)
    print(c)



def f(k,i,b,c):
    if i==len(b)-1:
        #print(k)
        if b[i] in k:
            pass
        else:
            z=k+b[i]
            if z in c:
                pass
            else:
                c.append(z)
                f(z,j,b,c)
    else:
        #print(k)
        for j in range(i+1,len(b)):
            if b[j] in k:
                continue
            else:
                z=k+b[j]
                if z in c:
                    continue
                else:
                    c.append(z)
                    f(z,j,b,c)

# Possibly define another function


#good_subsequences('aaabbb')

if __name__ == '__main__':
    import doctest
    doctest.testmod()

