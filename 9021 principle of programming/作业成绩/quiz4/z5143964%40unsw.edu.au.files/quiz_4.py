# Uses National Data on the relative frequency of given names in the population of U.S. births,
# stored in a directory "names", in files named "yobxxxx.txt with xxxx being the year of birth.
#
# Prompts the user for a first name, and finds out the first year
# when this name was most popular in terms of frequency of names being given,
# as a female name and as a male name.
# 
# Written by *** and Eric Martin for COMP9021


import os
import sys

first_name = input('Enter a first name: ')
directory = 'names'
min_male_frequency = 0
male_first_year = None
min_female_frequency = 0
female_first_year = None

# Replace this comment with your code

m_l=[]
fm_l=[]

for filename in os.listdir(directory):
  name_gender_count_list=[]
  male_list=[]
  female_list=[]
  count_male_list=[]
  count_female_list=[]
  if not filename.endswith('.txt'):   #filename!='yob1880.txt'filename.endswith('.txt')
    continue
  else:
  	#print(filename)
  	with open(directory+'/'+filename) as data_file:
  		for line in data_file:
  			line=line.strip('\n')
  			name,gender,count=line.split(',')
  			if gender=='M':
  				male_list.append([name,int(count)])
  				count_male_list.append(int(count))
  			else:
  				female_list.append([name,int(count)])
  				count_female_list.append(int(count))

      	#name_gender_count_list.append([name,gender,count])
      	
  #print('-------------------------------------male_list:\n',male_list)
  #print('-------------------------------------female_list:\n',female_list)
  #print('-------------------------------------count_male_list:\n',count_male_list)
  #print('-------------------------------------count_female_list:\n',count_female_list)
  		#max_male_count=max(count_male_list)
  		#max_female_count=max(count_female_list)
  		sum_male_count=sum(count_male_list)
  		sum_female_count=sum(count_female_list)
  		#print(filename)
  		#print('male_sum:',sum_male_count,'sum_female_count:',sum_female_count)
  		for i in range(len(male_list)):
  			if first_name==male_list[i][0]:# and max_male_count==male_list[i][1]:
  				frequency= (male_list[i][1]/sum_male_count)*100  #%
  				m_l.append([filename,frequency])
  		for i in range(len(female_list)):
  			if first_name==female_list[i][0]:# and max_female_count==female_list[i][1]:
  				frequency= (female_list[i][1]/sum_female_count)*100#%
  				fm_l.append([filename,frequency])
for i in range(len(m_l)):
	m_l[i][0]=int(m_l[i][0][3:7])
for i in range(len(fm_l)):
	fm_l[i][0]=int(fm_l[i][0][3:7])
m_l=sorted(m_l,key=lambda a: a[1],reverse=True)
fm_l=sorted(fm_l,key=lambda a: a[1],reverse=True)
#print('most_male_name:\n',m_l,'\n','most_female_name:\n',fm_l)

if m_l==[]:
	male_first_year = None
	min_male_frequency = 0
else:
	male_first_year=m_l[0][0]
	min_male_frequency = m_l[0][1]
if fm_l==[]:
	female_first_year = None
	min_female_frequency = 0
else:
	female_first_year=fm_l[0][0]
	min_female_frequency = fm_l[0][1]

#print(male_first_year,min_male_frequency)
#print(female_first_year,min_female_frequency)
#-------------------------------
if not female_first_year:
    print(f'In all years, {first_name} was never given as a female name.')
else:
    print(f'In terms of frequency, {first_name} was the most popular '
          f'as a female name first in the year {female_first_year}.\n'
          f'  It then accounted for {min_female_frequency:.2f}% of all female names.'
         )
if not male_first_year:
    print(f'In all years, {first_name} was never given as a male name.')
else:
    print(f'In terms of frequency, {first_name} was the most popular '
          f'as a male name first in the year {male_first_year}.\n'
          f'  It then accounted for {min_male_frequency:.2f}% of all male names.'
         )

