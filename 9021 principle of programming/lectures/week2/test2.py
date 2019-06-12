'''
nb_of_times=input('how many time...')
nb_of_times

correct_input=False
while not correct_input:
	nb_of_times=input('how many time do you ...')
	#nb_of_times=int(nb_of_times)
	if nb_of_times.isdigit():
		nb_of_times=int(nb_of_times)
		correct_input=True
		print(nb_of_times)
		break
while True:
	switches= input('want to switch?')
	if switches in {'YES','Yes','yes','y','Y'}:
	# if switches.lower() in {'yes','y'}
		switches=True
		break
	elif switches in {'NO','No','no','N','n'}:
		switches=False
		break
	else:
		print('wrong input, try again!')
#dir(str)


#dir(random)
#help(random.choice)
from random import choice
doors= ['A','B','C']
winning_door= choice(doors)
print(winning_door)
#dir()
#help(list.pop)    help(list.remove)
#first_choice=remove(choice(doors))   wrong
first_choice=choice(doors)
print(first_choice)
#first_choice=doors.remove(first_choice) 
doors.remove(first_choice) 
#print(first_choice)
print(doors)
if winning_door==first_choice:
	opended_door=choice(doors)
	doors.remove(opended_door)
	if not switches:
		second_choice=first_choice
	else:
		second_choice=doors[0]
else:
	doors.remove(winning_door)
	opended_door=doors[0]
	if not switches:
		second_switches=first_choice
	else:
		second_choice=doors[0]

'''
def f(a,b):
	print(a,b)
f(2,3)
f(*(2,3))
f(2,*(3,))
f(1,*(1,2,3,4,5,6))

set()
sort()







