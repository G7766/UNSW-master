'''
is_valid_prefix_expression(expression) checks whether the string expression
represents a correct infix expression (where arguments follow operators).

evaluate_prefix_expression(expression) returns the result of evaluating expression.

For expression to be syntactically correct:
- arguments have to represent integers, that is, tokens that can be converted to an integer
  thanks to int();
- operators have to be any of +, -, * and /;
- at least one space has to separate two consecutive tokens.

Assume that evaluate_prefix_expression() is only called on syntactically correct expressions,
and that / (true division) is applied to a denominator that is not 0.

You might find the reversed() function, the split() string method,
and the pop() and append() list methods useful.
'''

from operator import add, sub, mul, truediv
from copy import deepcopy

class ListNonEmpty(Exception):
    pass


def is_valid_prefix_expression(expression):
    '''
    >>> is_valid_prefix_expression('12')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ 12 4')
    Correct prefix expression
    >>> is_valid_prefix_expression('- + 12 4 10')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ - + 12 4 10 * 11 4')
    Correct prefix expression
    >>> is_valid_prefix_expression('/ + - + 12 4 10 * 11 4 5')
    Correct prefix expression
    >>> is_valid_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
    Correct prefix expression
    >>> is_valid_prefix_expression('twelve')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('2 3')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ + 2 3')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ / 1 2 *3 4')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ +1 2')
    Correct prefix expression
    >>> is_valid_prefix_expression('++1 2')
    Incorrect prefix expression
    >>> is_valid_prefix_expression('+ +1 -2')
    Correct prefix expression
    '''
    stack = []
    try:
        expression=expression.split()
        #print(expression)
        # Replace pass above with your code
    # - IndexError is raised in particular when trying to pop from an empty list
    # - ValueError is raised in particular when trying to convert to an int
    #   a string that cannot be converted to an int
    # - ListNonEmpty is expected to be raised when a list is found out not to be empty

    except (IndexError, ValueError, ListNonEmpty):
        print('Incorrect prefix expression')
    else:
        print('Correct prefix expression')
    return expression


def evaluate_prefix_expression(expression):
    '''
    >>> evaluate_prefix_expression('12')
    12
    >>> evaluate_prefix_expression('+ 12 4')
    16
    >>> evaluate_prefix_expression('- + 12 4 10')
    6
    >>> evaluate_prefix_expression('+ - + 12 4 10 * 11 4')
    50
    >>> evaluate_prefix_expression('/ + - + 12 4 10 * 11 4 5')
    10.0
    >>> evaluate_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
    8.0
    >>> evaluate_prefix_expression('+ +1 2')
    3
    >>> evaluate_prefix_expression('+ +1 -2')
    -1
    '''
    expression=is_valid_prefix_expression(expression)
    operation=['+','-','*','/']
    for x in range(len(expression)):
        if expression[x] not in operation:
            expression[x]=int(expression[x])
    #print(expression)
    z=calculate(expression)
    return z






def calculate(expression):
    operation=['+','-','*','/']
    ll=deepcopy(expression)
    #print(expression)
    for i in range(len(expression)):
        if expression[i] in operation:
            continue
        elif expression[i] not in operation and expression[i+1] not in operation:
            if expression[i-1]=='+':
                z=expression[i] + expression[i+1]
            if expression[i-1]=='-':
                z=expression[i] - expression[i+1]
            if expression[i-1]=='*':
                z=expression[i] * expression[i+1]
            if expression[i-1]=='/':
                z=expression[i] / expression[i+1]
            ll[i] = z
            #print(ll[i])
            del ll[i-1] #长度缩短了1
            del ll[i]
            if len(ll)==1:
                return ll[0]
            else:
                return calculate(ll)
        elif expression[i] not in operation and expression[i+1] in operation:
            continue
    


z=evaluate_prefix_expression('+ / + - + 12 4 10 * 11 4 5 - 80 82 ')
print(z)

    # Insert your code here
 





'''
if __name__ == '__main__':
    import doctest
    doctest.testmod()   
'''









'''
def calculate1(k):
    if k==2:
        return 2
    if k>2:
        k=k-1
        return calculate1(k)

p=calculate1(10)
print(p)
'''


