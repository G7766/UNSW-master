# Written by Eric Martin for COMP9021


'''
Prints out a conversion table of temperatures from Celsius to Fahrenheit degrees,
the former ranging from 0 to 100 in steps of 10.
'''


min_temperature = 0
max_temperature = 100
step = 10

print('Celsius\tFahrenheit')
for celsius in range(min_temperature, max_temperature + step, step):
    fahrenheit = celsius // 5 * 9 + 32
    print(f'{celsius:7d}\t{fahrenheit:10d}')


a=9/7
b=5.206
c=5.000
print(a)
print('---round---')
print(round(a,2))
print(round(b,2))
print(round(c,2))
print('------')
print('%.2f' % a)
print('%.2f' % b)
print('%.2f' % c)
print('------')
print(float('%.2f' % a))
print(float('%.2f' % b))
print(float('%.2f' % c))
from math import ceil,floor
#向上取整
print(ceil(a))
#向下取整
print(floor(a))






