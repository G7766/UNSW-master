import pandas as pd
from pandas import Series
import numpy as np
import requests
import matplotlib.pyplot as plt


def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    if print_column:
        print(", ".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            print(", ".join([str(row[column]) for column in dataframe]))




def q1_merge(dataframe1, dataframe2):
    #df = pd.merge(dataframe1, dataframe2, how='left', left_on=dataframe1.index, right_on=dataframe2.index)
    df = pd.merge(dataframe1, dataframe2, how='left', left_index=True, right_index=True,suffixes = ['_x', '_y'])
    df_q1 = df.head(5)
    print('Q1:\n')
    print_dataframe(df_q1, print_column=True, print_rows=True)
    return df
def q2_query_country(dataframe):
    print('----------------------------------------------------')
    print('Q2:\n ',dataframe.index[0])
    #print_dataframe(dataframe, print_column=True, print_rows=True)
def q3_Remove_rubish(dataframe):
    df = dataframe.drop(columns = 'Rubish')
    #print('Q3:\n ', df.head(5))
    print('----------------------------------------------------')
    print('Q3:\n ')
    print_dataframe(df.head(5), print_column=True, print_rows=True)
def q4_remove_nanValue(dataframe):
    df = dataframe.dropna(axis=0)
    #print('Q4:\n',df.tail(10))
    print('----------------------------------------------------')
    print('Q4:\n')
    print_dataframe(df.tail(10), print_column=True, print_rows=True)
def q5_most_goal(dataframe):
    #q5 = dataframe.groupby(dataframe.index)['Gold_x'].max()
    dataframe = dataframe[:-1]      #except the Total row
    new_date = df['Gold_x']
    new_date = pd.to_numeric(new_date)
    df['Gold_x'] = new_date
    #q5 = dataframe['Gold_x'].max()
    #print(q5)
    m = dataframe.index[dataframe['Gold_x']==dataframe['Gold_x'].max()]
    print('----------------------------------------------------')
    print('Q5:\n Country:',m[0], '\n Value:',dataframe['Gold_x'].max())

def q6_big_diff(dataframe):
    dataframe = dataframe[:-1]
    dataframe = dataframe[['Gold_x','Gold_y']]
    dataframe['Gold_x'] = pd.to_numeric(dataframe['Gold_x'], errors='ignore')
    dataframe['Gold_y'] = pd.to_numeric(dataframe['Gold_y'], errors='ignore')
    #.loc
    dataframe['difference'] = (dataframe['Gold_x'] - dataframe['Gold_y']).abs()
    dif_max = dataframe['difference'].max()
    #print("**************")
    #print(dataframe['difference'])
    print('----------------------------------------------------')
    print('Q6:\n','Country: ',dataframe['difference'].idxmax(), '\nDifference: ', dif_max)

def q7(dataframe):
    dataframe['Total_x'] = pd.to_numeric(dataframe['Total_x'], errors='ignore')
    dataframe['Total_y'] = pd.to_numeric(dataframe['Total_y'], errors='ignore')
    dataframe['Total.1'] = pd.to_numeric(dataframe['Total.1'], errors='ignore')
    dataframe['Total'] = dataframe['Total_x'] + dataframe['Total_y'] + dataframe['Total.1']
    dataframe = dataframe.sort_values(by='Total', ascending=False)
    #print('First 5 rows:',dataframe.head(5))
    print('----------------------------------------------------')
    print('Q7:\n')
    print('First 5 rows:\n')
    print_dataframe(dataframe.head(5), print_column=True, print_rows=True)
    #print('Last 5 rows:', dataframe.tail(5))
    print('Last 5 rows:\n')
    print_dataframe(dataframe.tail(5), print_column=True, print_rows=True)
    return dataframe

def q8_plot(dataframe):
    dataframe = dataframe[1:]
    dataframe = dataframe.head(10)
    df = dataframe[['Total_x','Total_y']]
    '''
    p1 = dataframe['Total_x']
    print(p1)
    p1.plot.barh()
    plt.show()
    
    p2 = dataframe['Total_y']
    p2.plot.barh()
    plt.show()
    '''
    #print(df.index.data)
    #help(dataframe.index)
    #plt.title('Medal for Winter and Summer Games')
    df = df.rename(columns={"Total_x": "Summer_Games", "Total_y": "Winter_Games"})
    df.plot.barh(y=['Summer_Games','Winter_Games'],stacked=True,title='Medal for Winter and Summer Games')
    plt.show()

    #df.plot.barh(y=['Total_x', 'Total_y'], stacked=True, title='Medal for Winter and Summer Games')
    # df.plot.bar(y='Total_y',ax=ax)
    print('----------------------------------------------------')
    print('Q8:.\n')
    print('8 finished.\n')


def q9_plot(dataframe):
    dataframe['Gold_y'] = pd.to_numeric(dataframe['Gold_y'], errors='ignore')
    dataframe['Silver_y'] = pd.to_numeric(dataframe['Silver_y'], errors='ignore')
    dataframe['Bronze_y'] = pd.to_numeric(dataframe['Bronze_y'], errors='ignore')
    dataframe = dataframe[['Gold_y','Silver_y','Bronze_y']]
    l=['United States','Australia','Great Britain','Japan','New Zealand']
    for i in l:
        for j in dataframe.index:
            if i in j:
                dataframe = dataframe.rename(index={j:i})

    s =Series(l)
    #df = dataframe.query('index == "United States" or "Australia" or "Great Britain" or "Japan" or "New Zealand"')
    dataframe = dataframe.loc[s]
    #print(dataframe)
    print('----------------------------------------------------')
    print('Q9:\n')
    print('Q9 finish.\n')
    dataframe.plot.bar(title='Medals for WinterGames',rot=0)
    plt.show()









if __name__ == '__main__':
    print('----------------------------------------------------')
    pd.set_option('display.max_columns', None, 'display.max_rows', None)

    f1 = 'Olympics_dataset1.csv'
    df1 = pd.read_csv(f1,index_col=0 ,skiprows=1,thousands=',')
    f2 = 'Olympics_dataset2.csv'
    df2 = pd.read_csv(f2,index_col=0 ,skiprows=1,thousands=',')


    # q1
    df = q1_merge(df1,df2)

    # q2 Set the index as the country name and then display the first country in the Dataframe.
    q2_query_country(df)

    # q3 Remove the rubish column and display the first five rows.
    q3_Remove_rubish(df)

    # q4 Remove the rows with NaN fields and display the last ten rows.
    q4_remove_nanValue(df)
    # q5 Calculate and display which country has won the most gold medals in summer games?
    q5_most_goal(df)

    # q6 Calculate and display which country had the biggest difference between their summer and winter gold medal?
    q6_big_diff(df)

    # q7 Sort the countries in descending order,
    # according to the number of total of medals earned throughout
    # the history and display the first and last 5 rows.
    df_7 = q7(df)


    # q8 Plot a bar chart of the top 10 countries
    # (according to the sorting in Question 7).
    # For each country use a stacked bar chart showing for each county the total medals
    # for winter and summer games.
    # See example chart below:
    df_8 = df_7
    q8_plot(df_8)

    # q9 Plot a bar chart of the countries (United States, Australia,
    # Great Britain, Japan, New Zealand).
    # For each county you need to show the gold,
    # silver and bronze medals for winter games.
    df_9 = df_7
    q9_plot(df_9)
