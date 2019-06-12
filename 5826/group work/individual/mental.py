import pandas as pd,numpy as np, os, gc, matplotlib.pyplot as plt, seaborn as sb, re, warnings, calendar, sys
from numpy import arange

def read(file):
    try:
        data = pd.read_csv(file)
    except:
        data = pd.read_csv(file, encoding='latin-1')
    return read_clean(data)


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

def head(data, n=10): return data.head(n)
def exclude(data, col):
    '''Only returns a dataframe where the columns in col are not included'''
    if type(col) is str: col = [col]
    columns = list(data.columns)
    leave = list(set(columns) - set(col))
    return data[leave]

def process_data1(dataframe):
    #gender:
    gender = []
    for i in dataframe.gender:
        if i =='male' or i == 'Male'or i=='MALE' or i=='m' or i=='M' or 'man' in i or 'Man' in i or 'Male' in i:
            gender.append('Male')
            continue
        elif i == 'f' or i == 'F' or i == 'female' or i=='Female' or i=='FEMALE' or 'woman' in i or 'Woman' in i or 'female' in i or 'Female' in i:
            gender.append('Female')
            continue
        else:
            gender.append('Unknow')

    print(len(gender))
    dataframe.gender = gender
    #dataframe = exclude(dataframe,['no_employees','anonymity','comments'])
    #dataframe = exclude(dataframe, 'timestamp')
    dataframe = dataframe.drop(columns=['no_employees','anonymity','comments'])
    return dataframe



def encoding_process(data):
    # data
    from sklearn import preprocessing
    from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
    # Encoding data
    labelDict = {}
    for feature in data:
        if feature == 'age':
            continue
        le = preprocessing.LabelEncoder()
        le.fit(data[feature])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        data[feature] = le.transform(data[feature])
        # Get labels
        labelKey = 'label_' + feature
        labelValue = [*le_name_mapping]
        labelDict[labelKey] = labelValue

    for key, value in labelDict.items():
        print(key, value)

    # Get rid of 'Country'
    data = data.drop(['country'], axis=1)
    data


def logisticRegression():
    from sklearn.linear_model import LogisticRegression
    # train a logistic regression model
    M_model = LogisticRegression()
    M_model.fit(X_train, y_train)

    # make class predictions for the testing set
    y_pred_class = M_model.predict(X_test)

    print('########### Logistic Regression ###############')

    accuracy_score = evalClassModel(M_model, y_test, y_pred_class, True)

    # Data for final graph
    methodDict['Log. Regres.'] = accuracy_score * 100


def split_data_set(data)
    from sklearn.model_selection import train_test_split
    # spilt the data
    # define X and y
    feature_cols = ['age', 'gender', 'family_history', 'benefits', 'care_options', 'leave', 'work_interfere']
    X = data[feature_cols]
    y = data.treatment

    # split X and y into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)
    return X_train, X_test, y_train, y_test


if __name__ =='__main__':
    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    file1 = 'survey.csv'

    file1_data = read(file1)
    print('*******************************************')
    #print(head(file1_data,5))


    print('*******************************************')
    data1 = process_data1(file1_data)
    #print(head(data1, 5))
    data1.to_csv('survey_new.csv')

