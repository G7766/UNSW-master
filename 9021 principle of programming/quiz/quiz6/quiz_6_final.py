# Defines two classes, Point() and Triangle().
# An object for the second class is created by passing named arguments,
# point_1, point_2 and point_3, to its constructor.
# Such an object can be modified by changing one point, two or three points
# thanks to the method change_point_or_points().
# At any stage, the object maintains correct values
# for perimeter and area.
#
# Written by *** and Eric Martin for COMP9021


from math import sqrt


class PointError(Exception):
    def __init__(self, message):
        self.message = message


class Point():
    def __init__(self, x = None, y = None):
        if x is None and y is None:
            self.x = 0
            self.y = 0
        elif x is None or y is None:
            raise PointError('Need two coordinates, point not created.')
        else:
            self.x = x
            self.y = y
            
    # Possibly define other methods


class TriangleError(Exception):
    def __init__(self, message):
        self.message = message

#-------------
def can_be_triangle(p1,p2,p3):
    be_triangle=((p1.x-p2.x)*(p3.y-p2.y)-(p3.x-p2.x)*(p1.y-p2.y))
    if be_triangle==0:
        return 0
    else:
        return 1
def per(x1,y1,x2,y2,x3,y3):
    perimeter1=sqrt((x1-x2)**2+(y1-y2)**2)
    perimeter2=sqrt((x2-x3)**2+(y2-y3)**2)
    perimeter3=sqrt((x1-x3)**2+(y1-y3)**2)
    perimeter=perimeter1+perimeter2+perimeter3
    return perimeter
#--------------

class Triangle:
    def __init__(self, *, point_1, point_2, point_3):
        '''
        #(x-x1)/(x2-x1)=(y-y1)/(y2-y1)
        #y-y2=((x-x1)/(x2-x1))*(y2-y1)
        #y=((x-x1)/(x2-x1))*(y2-y1)+y2
        #y=x*(y2-y1)/(x2-x1) - x1*(y2-y1)/(x2-x1) +y2
        #a=(y2-y1)/(x2-x1)
        #b=y2-x1*(y2-y1)/(x2-x1)
        self.a=(point_2.y-point_1.y)/(point_2.x-point_1.x)
        self.b=point_1.y-(point_1.x)/(point_2.y-point_1.y)
        if point_1.x==point_2.x and point_1.y==point_2.y:
            raise TriangleError('Incorrect input, triangle not created.')
        elif point_2.x==point_3.x and point_2.y==point_3.y:
            raise TriangleError('Incorrect input, triangle not created.')
        elif point_1.x==point_3.x and point_1.y==point_3.y:
            raise TriangleError('Incorrect input, triangle not created.')
        elif point_3.y==point_3.x*self.a+self.b:
            raise TriangleError('Incorrect input, triangle not created.')
        '''
        q=can_be_triangle(point_1, point_2, point_3)
        if q==0:
            raise TriangleError('Incorrect input, triangle not created.')
        else:
            self.point_1=point_1
            self.point_2=point_2
            self.point_3=point_3
            self.perimeter=per(self.point_1.x,self.point_1.y,self.point_2.x,self.point_2.y,self.point_3.x,self.point_3.y)
            self.area=abs((self.point_1.x*(self.point_2.y-self.point_3.y)+\
                            self.point_2.x*(self.point_3.y-self.point_1.y)+\
                                self.point_3.x*(self.point_1.y-self.point_2.y))/2)
        # Replace pass above with your code
    
    #def perimeter(self):
        #perimeter=per(self.point_1.x,self.point_1.y,self.point_2.x,self.point_2.y,self.point_3.x,self.point_3.y)
        #self.perimeter=perimeter
        '''
        p=sqrt((self.point_1.x-self.point_2.x)**2+(self.point_1.y-self.point_2.y)**2)+\
            sqrt((self.point_1.x-self.point_3.x)**2+(self.point_1.y-self.point_3.y)**2)+\
                sqrt((self.point_2.x-self.point_3.x)**2+(self.point_2.y-self.point_3.y)**2)
        '''
        #return perimeter


    '''
    def area(self):
        a=abs((self.point_1.x*(self.point_2.y-self.point_3.y)+ \
            self.point_2.x*(self.point_3.y-self.point_1.y)+\
                self.point_3.x*(self.point_1.y-self.point_2.y))/2)
        return a
    '''
       
    def change_point_or_points(self, *, point_1 = None,point_2 = None, point_3 = None):
        #method(1)
        if point_1 is not None:
            m=can_be_triangle(point_1, self.point_2, self.point_3)
            if m==0:
                print('Incorrect input, triangle not modified.')
            else:
                self.point_1=point_1
                self.perimeter=per(self.point_1.x,self.point_1.y,self.point_2.x,self.point_2.y,self.point_3.x,self.point_3.y)
                self.area=abs((self.point_1.x*(self.point_2.y-self.point_3.y)+\
                            self.point_2.x*(self.point_3.y-self.point_1.y)+\
                                self.point_3.x*(self.point_1.y-self.point_2.y))/2)
        if point_2 is not None:
            m=can_be_triangle(self.point_1, point_2, self.point_3)
            if m==0:
                print('Incorrect input, triangle not modified.')
            else:
                self.point_2=point_2
                self.perimeter=per(self.point_1.x,self.point_1.y,self.point_2.x,self.point_2.y,self.point_3.x,self.point_3.y)
                self.area=abs((self.point_1.x*(self.point_2.y-self.point_3.y)+\
                            self.point_2.x*(self.point_3.y-self.point_1.y)+\
                                self.point_3.x*(self.point_1.y-self.point_2.y))/2)
        if point_3 is not None:
            m=can_be_triangle(self.point_1, self.point_2, point_3)
            if m==0:
                print('Incorrect input, triangle not modified.')
            else:
                self.point_3=point_3
                self.perimeter=per(self.point_1.x,self.point_1.y,self.point_2.x,self.point_2.y,self.point_3.x,self.point_3.y)
                self.area=abs((self.point_1.x*(self.point_2.y-self.point_3.y)+\
                            self.point_2.x*(self.point_3.y-self.point_1.y)+\
                                self.point_3.x*(self.point_1.y-self.point_2.y))/2) 
        '''method(2)
        r=[point_1,point_2,point_3]
        print('r:',r)
        rr=[self.point_1,self.point_2,self.point_3]
        print('rr:',rr)
        for i in range(len(r)):
            if r[i]==None:
                pass
            else:
                rr[i]=r[i]
        m=can_be_triangle(rr[0], rr[1], rr[2])
        if m==0:
            print(m)
            raise TriangleError('Incorrect input, triangle not created.')
        else:
            print(m)
            self.point_1=rr[0]
            self.point_2=rr[1]
            self.point_3=rr[2]
        '''
        # Replace pass above with your code

    # Possibly define other methods
        

            
            