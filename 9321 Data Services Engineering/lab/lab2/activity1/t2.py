import pandas as pd
import numpy as np

raw_data1 = {'first_name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'last_name': ['Miller', 'Jacobson', ".", 'Milner', 'Cooze'],
        'age': [42, 52, 36, 24, 73],
        'preTestScore': [4, 24, 31, ".", "."],
        'postTestScore': ["25,000", "94,000", 57, 62, 70]}

raw_data2 = [{'c1':10, 'c2':100}, {'c1':11,'c2':110}, {'c1':12,'c2':120}]

df1 = pd.DataFrame(raw_data1)
print(df1)
df2 = pd.DataFrame(raw_data2)
print(df2)


print('Here is iterrows way:')
for index, row in df2.iterrows():
    print(row["c1"], row["c2"])


print('Here is iterrows way:')
for index, row in df1.iterrows():
    print(row["first_name"], row["last_name"])


