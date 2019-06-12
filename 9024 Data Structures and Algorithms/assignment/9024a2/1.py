def Age_process(dataframe):
    #print(head(dataframe.ageuponoutcome,5))
    new_age=[]
    for i in dataframe.ageuponoutcome:
        if type(i) ==str:
            l = i.split()
            if l[1] == 'years' or l[1]=='year':
                z = int(l[0])*365
                new_age.append(z)
            elif l[1] == 'months' or l[1]=='month':
                z = int(l[0]) * 30
                new_age.append(z)
            elif l[1] == 'weeks' or l[1]=='week':
                z = int(l[0])*7
                new_age.append(z)
            elif l[1] == 'days' or l[1] == 'day':
                z = int(l[0])
                new_age.append(z)
        else:
            new_age.append(0)

    #print(new_age)
    #print(len(new_age))
    dataframe.ageuponoutcome = new_age
    #print(dataframe.ageuponoutcome)
    return dataframe

def processcolor(data):
    new_color=[]
    for i in data.color:
        if '/' in i:
            new_color.append(1)
        else:
            new_color.append(0)
    data.color = new_color
    #print(data.color)
    return data


def sex_process(dataframe):
    l=[]
    for i in dataframe.sexuponoutcome:
        if i not in l:
            l.append(i)
    #print(l)
    new_sex= []
    for i in dataframe.sexuponoutcome:
        if type(i) ==str:
            if i=='Neutered Male':
                new_sex.append(1)
            elif i=='Spayed Female':
                new_sex.append(2)
            elif i=='Intact Male':
                new_sex.append(3)
            elif i=='Intact Female':
                new_sex.append(4)
            elif i=='Unknown':
                new_sex.append(0)
            else:
                new_sex.append(0)
        else:
            new_sex.append(0)
    #print(len(new_sex))
    dataframe.sexuponoutcome = new_sex
    return dataframe
def outcome_type_process(dataframe):
    l=[]
    for i in dataframe.outcometype:
        if i not in l:
            l.append(i)
    #print(l)
    new_type= []
    for i in dataframe.outcometype:
        if type(i) ==str:
            if i=='Return_to_owner':
                new_type.append(1)
            elif i=='Euthanasia':
                new_type.append(2)
            elif i=='Adoption':
                new_type.append(3)
            elif i=='Transfer':
                new_type.append(4)
            elif i=='Died':
                new_type.append(5)
            else:
                new_type.append(0)
        else:
            new_type.append(0)
    #print(len(new_type))
    dataframe.outcometype = new_type
    return dataframe




############################################

# data = clean(data)
# data = exclude(data, 'animalid')
# data = exclude(data,'name')
# data = exclude(data,'datetime')
# data = exclude(data,'outcomesubtype')
data= exclude(data,['animalid','name','datetime','outcomesubtype','breed'])
data = replace(data, [['Dog',1], ['Cat',2]])
age_process_df = Age_process(data)
#print(head(age_process_df,10))
color_process_data = processcolor(age_process_df)
#print(head(color_process_data, 10))
sex_process_data = sex_process(color_process_data)
#print(head(sex_process_data, 10))
data = outcome_type_process(sex_process_data)
#print(head(outcome_type_process_data, 10))

data

