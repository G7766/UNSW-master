
# coding: utf-8

# In[57]:


from math import sqrt
class SecondOrderEquationException(Exception):
    def __init__(self,message):
        self.message=message
    
    
class SecondOrderEquation(object):
    #def __init__(self):
    #def __init__(self,*,a=1,b=0,c=0):
    def __init__(self,a,b,c):
        #self.a=1
        #self.b=-3
        #self.c=2
        if a==0:
            raise SecondOrderEquationException('a should not be set to 0')
        self.a=a
        self.b=b
        self.c=c
        self.root_1,self.root_2=self._compute_roots()
    def __repr__(self):
        return f'SecondOrderEquation(a={self.a},b={self.b},c={self.c})'
    def __str__(self):
        #return 'AHA!'
        output_string=''
        if self.a==1:
            output_string='x^2'
        if self.a==-1:
            output_string='-x^2'
        else:
            output_string=f'{self.a}x^2'
        if self.b==1:
            output_string +='+x'
        elif self.b==-1:
            output_string +='-x'
        elif self.b>0 :
            output_string +=f'+{self.b}x'
        elif self.b<0 :
            output_string +=f'- {-self.b}x'
        if self.c>0:
            output_string +=f'+{self.c}'
        if self.c<0:
            output_string +=f'- {-self.c}'
        output_string +='=0'
        return output_string
            
        
    def _compute_delta(self):
        return self.b**2 - 4*self.a*self.c
    def _compute_roots(self):
        delta=self._compute_delta()
        if delta<0:
            return None,None
        if delta==0:
            root=-self.b/(2*self.a)
            return root,root
        root_1=(-b-sqrt(delta))/(2*self.a)
        root_2=(-b+sqrt(delta))/(2*self.a)
        return root_1,root_2
    def change_equation(self,*,a=None,b=None,c=None):
            
        if a ==0:
            raise SecondOrderEquationException('a should not be set to 0')
        if a is not None:
            self.a=a
        if b is not None:
            self.b=b
        if c is not None:
            self.c=c
        self.root_1,self.root_2=self._compute_roots()

class SecondOrderEquations(object):
    def __init__(self,equations):
        self.equations=equations
    
#SOE_1=SecondOrderEquation()
#print(SOE_1.a)
#SOE_1.compute_roots()
#print(SOE_1.compute_roots())
SOE_1=SecondOrderEquation(a=1,b=7,c=-4)
print(SOE_1.a)
print(SOE_1.b)
print(SOE_1.c)
#SOE_1.compute_roots()
print(SOE_1)
print('???',SOE_1.root_1,SOE_1.root_2)
try:
    SOE_1=SecondOrderEquation(a=0,b=7,c=-4)
except SecondOrderEquationException as m:
    print(m)
try:
    SOE_1.change_equation(a=0,b=7,c=-4)
except SecondOrderEquationException as m:
    print(m)
    
SOE1=SecondOrderEquationException(a=1,b=4,c=5)
SOE2=SecondOrderEquationException(a=1,b=-3,c=5)
q=SecondOrderEquations(SOE1,SOE2)
print(q())

