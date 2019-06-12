import pandas as pd
import numpy as np
import requests

file = 'Books.csv'

df = pd.read_csv(file)

def print_columns(dataframe):
    print(', '.join([column for column in dataframe]))
def print_rows(dataframe):
    for index, row in dataframe:
        print(', '.join([str(row(column)) for column in dataframe]))

# Task1
'''
axis : {0 or ‘index’, 1 or ‘columns’}, default 0

Axis along which the function is applied:

0 or ‘index’: apply function to each column.
1 or ‘columns’: apply function to each row.
'''
# Replace the cell value of "Place of Publication" with "London" if it contains "London",
    # and replace all '-' characters with space
    # We use the apply method which applies a lambda function to the cells of a dataframe

# method 1

df['Place of Publication'] = df['Place of Publication'].apply(
    lambda x:'London' if 'London' in x else x.replace('-',' ')
)
print(df['Place of Publication'])

# method 2 using numpy
'''
london = df['Place of Publication'].str.contains('London')
df['Place of Publication'] = np.where(london,'London',df['Place of Publication'].str.replace('-',' '))
print(df['Place of Publication'])
'''

# Task2

new_date = df['Date of Publication'].str.extract(r'^(\d{4})',expand=False)
# ^(\d{4}) : matches 4 digit numbers in the beginning of the string
df['Date of Publication'] = new_date
print('not numeric:\n',df['Date of Publication'])
print('******')
print(df['Date of Publication'][1])
print(type(df['Date of Publication'][1]))
print('******')

new_date = pd.to_numeric(new_date)    # to_numeric Convert argument to a numeric type.是把str型变成float
df['Date of Publication'] = new_date
print('numeric:\n',df['Date of Publication'])
print('******')
print(df['Date of Publication'][1])
print(type(df['Date of Publication'][1]))
print('******')

#Task 3
# replace all NaN with 0
new_date = new_date.fillna(0) # fillna 填空值 把Nan 换为0
df['Date of Publication'] = new_date
print(df['Date of Publication'])