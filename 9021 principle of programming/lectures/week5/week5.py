
# coding: utf-8

# In[ ]:


#dir(os)


# In[ ]:


import os
import sys
directory_name='names'
classified_directory_name=directory_name+'_classified'
if os.path.exists(classified_directory_name):
    print('Classified directory exists already')
    sys.exit()
os.mkdir(classified_directory_name)

male_directory_name = classified_directory_name+'/male'
female_directory_name =classified_directory_name + '/female'
os.mkdir(male_directory_name)
os.mkdir(female_directory_name)
for filename in os.listdir(directory_name):
    if not filename.endswith('.txt'):
        continue
    #opening 1 file for reading purposes
    # and 2 files for writing purposes
    with open(directory_name+ '/' +filename) as data_file,            open(male_directory_name+ '/' + filename,'w') as male_file,                open(female_directory_name + '/' + filename,'w') as female_file:
        #Processing each line in file taht i am reading
        for line in data_file:
            #eactracting th 3 fields from the line
            #print(line)
            #break
            #line.split(',')
            #line='Mary,F,20'
            #name,gender,age=line.split(',')
            name,gender,count=line.split(',')
            if gender=='F':
                print(','.join((name,count)),end='',file=female_file)
            else:
                print(','.join((name,count)),end='',file=male_file)
            


# In[ ]:


'''
l={'aa':[12]}
l('aa').append(3) # true
l('bb').append(3)#wrong
defaultdict
l=defaultdict(list)
l('bb').append(3)#true
'''


# In[ ]:


import os
import sys
from collections import defaultdict
directory_name='names'
years_by_name=defaultdict(list)
#print(sorted(os.listdir(directory_name)))
for filename in sorted(os.listdir(directory_name)):
    if not filename.endswith('.txt'):
        continue
    year=int(filename[3:7])
#opening 1 file for reading purposes
    # and 2 files for writing purposes
    with open(directory_name+ '/' +filename) as data_file,            open(male_directory_name+ '/' + filename,'w') as male_file,                open(female_directory_name + '/' + filename,'w') as female_file:
        #Processing each line in file taht i am reading
        for line in data_file:
            #eactracting th 3 fields from the line
            name,gender,count=line.split(',')
            if gender=='M':
                break
            years_by_name[name].append(year)
for gap,starting_year,name in sorted([(years_by_name[name][i+1]-years_by_name[name][i]],
                                       years_by_name[name][i],name) 
                                       for name in years_by_name 
                                       for i in range(len(years_by_name[name])-1)],
                                       reverse=True)[:10]:
    print(f'{name} was given in {starting_year}, and then [gap] years later')


# In[ ]:


D={'jone':2000,2001,2002,2003,'peter':1900,1998,1993,2011}
[D[name] for name in D]
[D[name][i] for name in D for i in range(len(D[name]))]
[D[name][i+1]-D[name][i] for name in D for i in range(len(D[name]))]
[(D[name][i+1]-D[name][i],D[name][i],name) for name in D for i in range(len(D[name]))]
sorted[(D[name][i+1]-D[name][i],D[name][i],name) for name in D for i in range(len(D[name])),reverse=True]




#--------
def g(p):
    return g[1]
sorted(L,key=lambda x: x[1],reverse=True)
sorted(L,key=g)

