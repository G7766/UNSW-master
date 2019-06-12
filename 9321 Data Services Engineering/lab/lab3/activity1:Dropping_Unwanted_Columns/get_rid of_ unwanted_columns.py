import pandas as pd
import requests
import numpy

file = 'Books.csv'
df = pd.read_csv(file)
#print(df)

def print_columns(dataframe):
    #for column in df:
    #    print(column)
    print(', '.join([column for column in dataframe]))

def print_rows(dataframe):
    #for index, row in df.iterrows():
    #    print(row)
    for index, row in dataframe.iterrows():
        print(', '.join([str(row[column]) for column in dataframe]))

def column_nullvalue(dataframe):
    s = dataframe
    s = s.isnull().sum()
    print(s)

def drop_columns_value(dataframe, drop_index):
    df = dataframe
    if type(drop_index) == str:
        df = df.drop(columns = drop_index)
        print(df)
    if type(drop_index) == list:
        df = df.drop(columns=drop_index)
        print(df)

'''
>>> df.drop(columns=['B', 'C'])
   A   D
0  0   3
1  4   7
2  8  11
'''
def drop_row_value(dataframe,drop_index):
    df = dataframe
    df = df.drop([drop_index])
    print(df)
'''
df.drop([0, 1])
   A  B   C   D
2  8  9  10  11
'''
#print_columns(df)
#print_rows(df)
column_nullvalue(df)
#drop_columns_value(df,'Title')
#drop_row_value(df,1)

l =['Edition Statement',
    'Corporate Author',
    'Corporate Contributors',
    'Former owner',
    'Engraver',
    'Contributors',
    'Issuance type',
    'Shelfmarks']
drop_columns_value(df,l)


