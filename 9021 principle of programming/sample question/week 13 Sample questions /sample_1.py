
def remove_consecutive_duplicates(word):
    '''
    >>> remove_consecutive_duplicates('')
    ''
    >>> remove_consecutive_duplicates('a')
    'a'
    >>> remove_consecutive_duplicates('ab')
    'ab'
    >>> remove_consecutive_duplicates('aba')
    'aba'
    >>> remove_consecutive_duplicates('aaabbbbbaaa')
    'aba'
    >>> remove_consecutive_duplicates('abcaaabbbcccabc')
    'abcabcabc'
    >>> remove_consecutive_duplicates('aaabbbbbaaacaacdddd')
    'abacacd'
    '''
    # Insert your code here (the output is returned, not printed out)    
    if word=='':
        return ''
    k=word[0]
    #c=word[0]          
    for i in range(len(word)-1):
        if i == len(word)-1:
            break
        if word[i]==word[i+1]:
            continue
        else:
            k = k + word[i+1]

    return k



if __name__ == '__main__':
    import doctest
    doctest.testmod()

'''
k=remove_consecutive_duplicates('a')
print(k)
'''
