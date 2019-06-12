import pandas as pd
import numpy as np
import requests

def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in dataframe]))


def print_columns(dataframe):
    #for column in df:
    #    print(column)
    print(', '.join([column for column in dataframe]))

def print_rows(dataframe):
    #for index, row in df.iterrows():
    #    print(row)
    for index, row in dataframe.iterrows():
        print(', '.join([str(row[column]) for column in dataframe]))


def clean(dataframe):
    df = dataframe
    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda x:'London' if 'London' in x else x.replace('-',' '))
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    df['Date of Publication'] = new_date

    df.columns = [c.replace(' ','_') for c in df.columns]

    return df


if __name__ == '__main__':
    file1 = 'Books.csv'
    df1 = pd.read_csv(file1)
    df1 = clean(df1)
    file2 = 'City.csv'
    df2 = pd.read_csv(file2)

    #task1
    #merge two dataframe
    df = pd.merge(df1, df2, how='left', left_on=['Place_of_Publication'], right_on=['City'])
    print(df.columns)

    #task2
    # Group by Country and keep the country as a column
    gb_df = df.groupby(['Country'],as_index=False)
    print(gb_df['Country'])

    #task3
    # Select a column (as far as it has values for all rows, you can select any column)
    df = gb_df['Identifier'].count()
    print(df)
    print_dataframe(df)