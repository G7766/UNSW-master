from random import seed, randint
import sys

def even(n):
    if n%2==0:
        return 1
    else:
        return 0
def f(arg_for_seed, nb_of_elements, max_element):
    if nb_of_elements < 0:
        sys.exit()
    seed(arg_for_seed)
    L = [randint(0, max_element) for _ in range(nb_of_elements)]
    print('Here is L:', L)
    R = []
    # Insert your code here
    l=[]
    n=len(L)
    for i in range(n):
        q=even(L[i])
        if q==1:
            l.append(i)
    print(l)
    lll=[]
    ll=[]
    nn=len(l)
    i=0
    for i in range(nn):
        m=[i,0]
        for j in range(i+1,nn):
            if l[i]+1==l[i+1]:
                m[-1]=l[i+1]
                #print(m[-1])
        if m[-1]==0:
            lll.append(L[l[0]])
        else:
            lll.append([L[l[0]:l[1]]])
    print(lll)
    '''
    while i<nn:
        m=[i,0]
        while l[i]==l[i]+1:
            m[-1]=i+1
            i=i+1
        lll.append(m)
        i=i+1
    print(lll)
    '''


        
            
            
            

    

    print('')
    print('The decomposition of L into longest sublists of even numbers is:', R)    



f(0,2,10)
q=even(2)
print(q)
if __name__ == '__main__':
    import doctest
    doctest.testmod()
