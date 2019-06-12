import pandas as pd
import numpy as np

raw_data = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}

df = pd.DataFrame(raw_data, columns = ['first_name', 'last_name', 'age', 'preTestScore', 'postTestScore'])
print(df)


print('****************************************************************')

#Save dataframe as csv in the working director
df.to_csv('pandas_dataframe_importing_csv/example.csv')

#Load a csv
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv')
print(df)

#Load a csv with no headers
print('******************************************************')
print('Load a csv with no headers:')

df = pd.read_csv('pandas_dataframe_importing_csv/example.csv',header = None)
print(df)

print('******************************************************')
#Load a csv while specifying column names
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv',
                 names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
print(df)

print('******************************************************')
#Load a csv with setting the index column to UID
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv', index_col='UID', names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
print(df)
print('******************************************************')
#Load a csv while setting the index columns to First Name and Last Name
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv', index_col=['First Name', 'Last Name'], names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
print(df)
print('******************************************************')
#Load a csv while specifying “.” as missing values
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv', na_values=['.'])
#pd.isnull(df)
print(pd.isnull(df)) #如果是'.' True else False
print('******************************************************')
#Load a csv while specifying “.” and “NA” as missing values in the Last Name column
# and “.” as missing values in Pre-Test Score column #将显示点和NA 视为no value
sentinels = {'Last Name': ['.', 'NA'], 'Pre-Test Score': ['.']}
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv',na_values=sentinels)
print(df)

print('******************************************************')
#Load a csv while skipping the top 3 rows

df = pd.read_csv('pandas_dataframe_importing_csv/example.csv',na_values=sentinels, skiprows=3)
print(df)

print('******************************************************')
#Load a csv while interpreting “,” in strings around numbers as thousands seperators
#把上面 数字string 中的千位分隔符'，'去掉
df = pd.read_csv('pandas_dataframe_importing_csv/example.csv', thousands=',')
print(df)


my_dataframe = df
print(my_dataframe)


print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
l=list(my_dataframe.columns.values)
print(l)
ll=[k for k in my_dataframe ]
print(ll)
for i in my_dataframe:
    print(i)
print('?????????????????????????????????????????????')
print(sorted(df))
