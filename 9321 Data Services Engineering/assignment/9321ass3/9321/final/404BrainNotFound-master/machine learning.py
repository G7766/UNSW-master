import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import precision_score, accuracy_score, recall_score

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

import sqlite3
import numpy as np

def load_match(match, split_percentage):

    match = shuffle(match)
    match_x = match.drop(columns=["Home", "Away", "home_result", "away_result"]).values
    match_y = match['home_result'].values

    # Split iris data in train and test data
    # A random permutation, to split the data randomly

    split_point = int(len(match_x) * split_percentage)
    match_X_train = match_x[:split_point]
    match_y_train = match_y[:split_point]
    match_X_test = match_x[split_point:]
    match_y_test = match_y[split_point:]

    return match_X_train, match_y_train, match_X_test, match_y_test

def determine_home_win_lose(match):
    if(match["home_team_goal"] > match["away_team_goal"]):
        return "win"
    elif(match["home_team_goal"] < match["away_team_goal"]):
        return "lose"
    else:
        return "draw"

def determine_away_win_lose(match):
    if(match["home_team_goal"] > match["away_team_goal"]):
        return "lose"
    elif(match["home_team_goal"] < match["away_team_goal"]):
        return "win"
    else:
        return "draw"


# def add_attribute_column(match, team_attribute, attribute_name):
#     match["Home"]

def getMatch(conn):
    match = pd.read_sql_query("SELECT home_team_api_id,away_team_api_id, home_team_goal, away_team_goal FROM Match;", conn)
    match = match.dropna()
    match.rename(columns={'home_team_api_id':'Home', 'away_team_api_id':'Away'}, inplace=True)

    match['home_result'] = match.apply(determine_home_win_lose, axis=1)
    match['away_result'] = match.apply(determine_away_win_lose, axis=1)
    match = match.drop(columns=["home_team_goal", "away_team_goal"])


    # team_attribute = pd.read_sql_query("SELECT team_api_id, buildUpPlaySpeed \
    #                     ,buildUpPlayPassing, chanceCreationPassing, chanceCreationCrossing \
    #                     ,chanceCreationShooting, defencePressure, defenceAggression, defenceTeamWidth FROM Team_Attributes;", conn)
    # team_attribute.fillna(50)

    team_attribute = pd.read_sql_query("SELECT team_api_id, buildUpPlaySpeed, buildUpPlayDribbling, \
        buildUpPlayPassing, chanceCreationPassing, chanceCreationCrossing, chanceCreationShooting, \
        defencePressure, defenceAggression, defenceTeamWidth FROM Team_Attributes;", conn)

    team_attribute = team_attribute.groupby("team_api_id").mean()
    team_attribute.fillna(50)
    #print(team_attribute)


    match = match.merge(team_attribute, how='left', left_on="Home", right_index=True)
    #match.rename(columns={'buildUpPlaySpeed':'Home_buildUpSpeed'}, inplace=True)
    match = match.merge(team_attribute, how='left', left_on="Away", right_index=True)
    #match.rename(columns={'buildUpPlaySpeed':'Away_buildUpSpeed'}, inplace=True)
    #match = match.drop(columns=["team_api_id_x", "team_api_id_y"])
    match = match.dropna()
    #print(match)
    return match

def regression_train(match_X_train, match_y_train):
    # train a classifier
    regre = LogisticRegression()
    regre.fit(match_X_train, match_y_train) 
    return regre

def regression_prediction(regre, match_X_test, match_y_test, match_input,pid):
    # predict the test set
    predictions = regre.predict(match_X_test)
    p = regre.predict(match_input)

    pred_json = {'prediction':p[0],
                'accuracy':accuracy_score(match_y_test, predictions)
                }
    print(type(pred_json))
    print(pred_json)

    print("confusion_matrix:\n", confusion_matrix(match_y_test, predictions))
    print("precision:\t", precision_score(match_y_test, predictions, average=None))
    print("recall:\t\t", recall_score(match_y_test, predictions, average=None))
    print("accuracy:\t", accuracy_score(match_y_test, predictions))
    return (pred_json)


if __name__ == '__main__':
    conn = sqlite3.connect("database.sqlite")

    match = getMatch(conn)
    # Split the data into test and train parts
    match_X_train, match_y_train, match_X_test, match_y_test = load_match(match, split_percentage=0.7)
    
    regression_prediction(match_X_train, match_y_train, match_X_test, match_y_test)

### envalueation part
### find out LogisticRegression has best performance
    classifiers = [KNeighborsClassifier(),
                   DecisionTreeClassifier(),
                   LinearDiscriminantAnalysis(),
                   LogisticRegression()
                   ]

    classifier_accuracy_list = []
    for i, classifier in enumerate(classifiers):
        # split the dataset into 5 folds; then test the classifier against each fold one by one
        accuracies = cross_val_score(classifier, match_X_train, match_y_train, cv=5)
        classifier_accuracy_list.append((accuracies.mean(), type(classifier).__name__))
        print("=================== finish ====="+ str(classifier)+"=====================")

    # sort the classifiers
    classifier_accuracy_list = sorted(classifier_accuracy_list, reverse=True)
    for item in classifier_accuracy_list:
        print(item[1], ':', item[0])
