#Temperature conversion tables

#display a conversion table from Celsius degrees to Fahrenheit degrees, with the former ranging from 0 to 100 in steps of 10

'''
min_temperature=0
max_temperature=300
step=20
print('Fahrenheit\t Celsius')  #\t :A tab
# We let fahrenheit take the values
# - min_temperature
# - min_temperature + step
# - min_temperature + 2 * step
# - min_temperature + 3 * step
# ...
# up to the largest value smaller than max_temperature + step

for fahrenheit in range(min_temperature,max_temperature+step,step):
	celsius = (fahrenheit-32)*5/9
	# {:10d}:  fahrenheit as a decimal number in a field of width 10
    # {:7.1f}: celsius as a floating point number in a field of width 7
    #          with 1 digit after the decimal point
    #print(f'{fahrenheit:10d}\t{celsius:7.1f}')
	print(f'{fahrenheit:10d}\t{celsius:7.1f}')
# Output an empty line 
print()
'''

'''
Prints out a conversion table of temperatures from Celsius to Fahrenheit degrees,
the former ranging from 0 to 100 in steps of 10.
'''

min_temperature=0
max_temperature=100
step=10
print('Fahrenheit\t Celsius')
for celsius in range(min_temperature,max_temperature+step,step):
	fahrenheit=celsius*9//5+32
	print(f'{celsius:7}\t{fahrenheit:10}')


