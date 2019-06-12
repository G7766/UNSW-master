
def f(N):
    '''
    >>> f(20)
    Here are your banknotes:
    $20: 1
    >>> f(40)
    Here are your banknotes:
    $20: 2
    >>> f(42)
    Here are your banknotes:
    $2: 1
    $20: 2
    >>> f(43)
    Here are your banknotes:
    $1: 1
    $2: 1
    $20: 2
    >>> f(45)
    Here are your banknotes:
    $5: 1
    $20: 2
    >>> f(2537)
    Here are your banknotes:
    $2: 1
    $5: 1
    $10: 1
    $20: 1
    $100: 25
    '''
    banknote_values = [1, 2, 5, 10, 20, 50, 100]
    banknotes = dict.fromkeys(banknote_values, 0)
    # Insert your code here
    b = [0]*len(banknote_values)
    for i in range(-1,-len(banknote_values)-1,-1):
        #print(':',N)
        #print('?',i)
        if N<banknote_values[i]:
            continue
        if N>=banknote_values[i]:
            z=N//banknote_values[i]
            #print('?',N)
            b[i]=z
            N=N % banknote_values[i]
    #print(b)
    banknotes=dict.fromkeys(banknote_values, 0)
    for i in range(len(banknote_values)):
        for value in banknotes:
            if banknote_values[i]==value:
                banknotes[value]=b[i]
        #if banknote_values[i]=banknotes[keys]
    #print(banknotes)
    
    print('Here are your banknotes:')
    for value in sorted(banknotes):
        if banknotes[value]:
            print('${}: {}'.format(value, banknotes[value]))
               


if __name__ == '__main__':
    import doctest
    doctest.testmod()


f(43)

'''
print(12138//100)
print(12138 % 100)
#for i in range(-1,-6,-1):
#    print(i)

#f(12138)
#f(2537)
#f(42)

d={1:2,2:3}
for value in d:
    print(value)
    print(d[value])
'''

