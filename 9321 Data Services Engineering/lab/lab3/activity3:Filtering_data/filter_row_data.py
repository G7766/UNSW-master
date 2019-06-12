import pandas as pd
import numpy as np
import requests

if __name__ =="__main__":
    file = 'Books.csv'
    df = pd.read_csv(file)
    
    # step1:London
    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda x:'London' if 'London' in x else x.replace('-',' '))
    print(df['Place of Publication'])

    # step2:
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})',expand=False)
    df['Date of Publication'] = new_date
    new_date = pd.to_numeric(new_date)
    df['Date of Publication'] = new_date

    # step3:
    new_date = df['Date of Publication'].fillna(0)
    df['Date of Publication'] = new_date
    print(df['Date of Publication'])


    # task
    print(df.columns)
    df.columns = [c.replace(' ','_') for c in df.columns]
    print(df.columns)

    #task query
    df2 = df.query('Date_of_Publication > 1866 and Place_of_Publication == "London"')
    print(df2)



