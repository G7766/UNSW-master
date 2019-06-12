import pandas as pd
import numpy as np
import os, gc
import matplotlib.pyplot as plt
import seaborn as sb
import re
import warnings
import calendar
import sys
from numpy import arange
import sklearn



#get_ipython().run_line_magic('matplotlib', 'inline')
warnings.filterwarnings('ignore')
np.set_printoptions(suppress=True)
pd.options.mode.chained_assignment = None
pd.set_option('display.float_format', lambda x: '%.3f' % x)




def head(data, n = 10): return data.head(n)


def show_trend(dataframe):
    #get Dog and Cat categories
    result_dog = dataframe[(dataframe.animaltype == "Dog")]
    result_cat = dataframe[(dataframe.animaltype == "Cat")]

    #change datetime to date_time
    result_dog['datetime'] = pd.to_datetime(result_dog['datetime'])
    result_cat['datetime'] = pd.to_datetime(result_cat['datetime'])

    #We only use year and month to analyse
    result_dog['datetime']=result_dog.datetime.map(lambda x: x.strftime('%Y-%m'))
    result_cat['datetime']=result_cat.datetime.map(lambda x: x.strftime('%Y-%m'))
    #print(result_dog)
    #for i in result_dog['datetime']:
    #    print(i.year)
    #print(head(result_dog,10))
    #print(head(result_cat, 10))

    #count and groud by year-month
    #count by range
    #df = pd.DataFrame({'datetime': pd.date_range(start=dt.datetime(2015, 12, 20), end=dt.datetime(2016, 3, 1))})
    print('************************COUNT**********************************')
    #count by year-month
    count_dog = result_dog.groupby([result_dog['datetime']]).agg({'count'})
    count_cat = result_cat.groupby([result_cat['datetime']]).agg({'count'})
    count_dog_by_date = count_dog['animaltype']
    #print('dog:',count_dog_by_date)
    count_cat_by_date = count_cat['animaltype']
    #print('cat:',count_cat_by_date)
    # plot the line char to show the trend
    df = pd.merge(count_dog_by_date, count_cat_by_date, how='left', left_index=True, right_index=True,suffixes = ['_dog', '_cat'])
    #print(df.head(10))
    #print(df.index)
    #df['time']= df.index.values
    #print(df)
    line = df.plot.line()
    plt.show()
    return result_dog,result_cat


def show_OutcomeType(dataframe):
    result_Return_to_Owner = dataframe[(dataframe.outcometype == "Return_to_owner")]
    result_Euthanasia = dataframe[(dataframe.outcometype == "Euthanasia")]
    result_Adoption = dataframe[(dataframe.outcometype == "Adoption")]
    result_Transfer = dataframe[(dataframe.outcometype == "Transfer")]
    count_Return_to_Owner = result_Return_to_Owner.groupby([result_Return_to_Owner['datetime']]).agg({'count'})
    count_Euthanasia = result_Euthanasia.groupby([result_Euthanasia['datetime']]).agg({'count'})
    count_Adoption = result_Adoption.groupby([result_Adoption['datetime']]).agg({'count'})
    count_Transfer = result_Transfer.groupby([result_Transfer['datetime']]).agg({'count'})

    count_Return_to_Owner = count_Return_to_Owner['outcometype']
    count_Euthanasia = count_Euthanasia['outcometype']
    count_Adoption = count_Adoption['outcometype']
    count_Transfer = count_Transfer['outcometype']

    df1 = pd.merge(count_Return_to_Owner, count_Euthanasia, how='left', left_index=True, right_index=True,
                  suffixes=['_Return_to_owner', '_Euthanasia'])
    df2 = pd.merge(count_Adoption, count_Transfer, how='left', left_index=True,
                  right_index=True,
                  suffixes=['_Adoption', '_Transfer'])
    df = pd.merge(df1, df2, how='left', left_index=True,
                  right_index=True)

    print(head(df,10))
    return df

def plot_OutcomeType(dataframe):
    line = dataframe.plot.line()
    plt.show()


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
    for i in range(len(new_age)):
        if new_age[i]<=35:
            new_age[i] = 2
            continue
        elif new_age[i]<=365:
            new_age[i] = 5
            continue
        elif new_age[i]<=365*3:
            new_age[i] = 2
            continue
        elif new_age[i]<=365*5:
            new_age[i] = 1
            continue
        elif new_age[i]<365*10:
            new_age[i] = 1
            continue
        elif new_age[i]>=365*10:
            new_age[i] = 0
            continue
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
    print(data.color)
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
    print(len(new_sex))
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
                new_type.append(9)
            elif i=='Euthanasia':
                new_type.append(1)
            elif i=='Adoption':
                new_type.append(10)
            elif i=='Transfer':
                new_type.append(8)
            elif i=='Died':
                new_type.append(2)
            else:
                new_type.append(0)
        else:
            new_type.append(0)
    #print(len(new_type))
    dataframe.outcometype = new_type
    return dataframe

def read_clean(data):
    data.columns = [str(x.lower().strip().replace(' ', '_')) for x in data.columns]
    seen = {};
    columns = [];
    i = 0
    for i, x in enumerate(data.columns):
        if x in seen:
            columns.append(x + '_{}'.format(i))
        else:
            columns.append(x)
        seen[x] = None

    for x in data.columns[data.count() / len(data) < 0.0001]: del data[x];
    gc.collect();
    try:
        data = data.replace({'': np.nan, ' ': np.nan});
    except:
        pass;

    if len(data) < 10000:
        l = len(data);
    else:
        l = 10000;
    sample = data.sample(l);
    size = len(sample);

    for x in sample.columns:
        ints = pd.to_numeric(sample[x], downcast='integer', errors='coerce')
        if ints.count() / size > 0.97:
            minimum = ints.min()
            if minimum > 0:
                data[x] = pd.to_numeric(data[x], downcast='unsigned', errors='coerce')
            else:
                data[x] = pd.to_numeric(data[x], downcast='integer', errors='coerce')
        else:
            floats = pd.to_numeric(sample[x], downcast='float', errors='coerce')
            if floats.count() / size > 0.97:
                data[x] = pd.to_numeric(data[x], downcast='float', errors='coerce')
            else:
                dates = pd.to_datetime(sample[x], errors='coerce')
                if dates.count() / size > 0.97: data[x] = pd.to_datetime(data[x], errors='coerce')
    return data.reset_index(drop=True)


def read(file):
    try:
        data = pd.read_csv(file)
    except:
        data = pd.read_csv(file, encoding='latin-1')
    return read_clean(data)

def delete_less_species(dataframe):
    l = []
    for i in dataframe.color:
        if i not in l:
            l.append(i)
    #print(l)
    #print(len(l))
    k=0
    ll= [0]*len(l)
    for i in dataframe.color:
        for j in range(len(l)):
            if l[j]==i:
                ll[j] = ll[j]+1
    #print(ll)
    type =[]
    for i in range(len(ll)):
        if ll[i]<=10:
            type.append(l[i])

    #print(type)
    for i in type:
        df = dataframe[dataframe.color!=i]



    return df









if __name__ == '__main__':
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    # 1 part
    file = 'train.csv'
    data = read(file)

    #print(head(data,10))

    #data = delete_less_species(data)
    #print(head(data, 10))

    data = Age_process(data)



    '''
    print('**********************TREND************************')
    df_dog,df_cat = show_trend(data)
    df_OutcomeType = show_OutcomeType(df_dog)
    plot_OutcomeType(df_OutcomeType)
    print('*****************************************************')
    


    # 2 part
    print('**********************2************************')
    data = exclude(data, ['animalid', 'name', 'datetime', 'outcomesubtype', 'breed'])
    print(data)


    # 3 part
    print('**********************3************************')
    data = Age_process(data)

    # 4 part
    print('**********************4************************')
    data['color'] = remove(data['color'], ' ')
    splits = split(data['color'], '/')
    print(head(splits, 10))

    # 5 part
    print('**********************5************************')
    color = tally(splits, multiple=True)

    # 6 part
    print('**********************6************************')
    sum_color = col_operation(color, 'sum')
    plot(x=sum_color, style='barplot')

    # 7 part
    print('**********************7************************')
    a = tally(data['sexuponoutcome'], multiple=True, method='count')
    print(head(a, 10))



    # 8 part
    print('**********************8************************')
    b = tally(data['animaltype'], multiple=True, minimum=3, method='count')
    print(head(b, 10))

    # 9 part
    print('**********************9************************')
    NewData = hcat(color, a, b)
    head(NewData, 10)
    data = outcome_type_process(data)
    Y = data['outcometype']

    # 10 part
    print('**********************10************************')
    model = Inference(logistic=False)
    model.fit(NewData, Y)

    # 11 part
    print('**********************11************************')
    result = model.coefficients()
    print(head(result, 10))
    # data = clean(data)
    # data = exclude(data, 'animalid')
    # data = exclude(data,'name')
    # data = exclude(data,'datetime')
    # data = exclude(data,'outcomesubtype')
    data = exclude(data, ['animalid', 'name', 'datetime', 'outcomesubtype', 'breed'])
    data = replace(data, [['Dog', 1], ['Cat', 2]])
    age_process_df = Age_process(data)
    # print(head(age_process_df,10))
    color_process_data = processcolor(age_process_df)
    # print(head(color_process_data, 10))
    sex_process_data = sex_process(color_process_data)
    # print(head(sex_process_data, 10))
    # print(head(outcome_type_process_data, 10))
    print(data)

    data = outcome_type_process(sex_process_data)
    Y = data['outcometype']
    X = exclude(data, 'outcometype')
    model = LinearModel(logistic=True, layers=1)
    model.fit(X, Y)
    model.score(model.predict(X), Y)
    model.plot(model.predict(X), Y)
    model.analyse()
    '''