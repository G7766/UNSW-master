import json
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity


def loadFont():
    f = open("db.json", encoding='utf-8')
    setting = json.load(f)
    dict = {}
    dict_name = {}
    id = {}
    count = 1
    for i in setting:
        #print(i)
        dict[i] = setting[i]['overview']
        dict_name[i] = setting[i]['name']
    for i in setting:
        id[i] = count
        count += 1
    return dict, id

description,id = loadFont()
#print(id)
frequency = {}
for i in description:
    divi = re.sub(r'[^A-Za-z0-9]+',' ',description[i])
    divi = divi.split(' ')
    for j in divi:
        if j in frequency.keys():
            frequency[j] += 1
        else:
            frequency[j] = 1
a = sorted(frequency.items(), key=lambda x: x[1], reverse = True)
#print(a)
'''
keyword:
security
data
software
algorithm
research
applications
networks
distributed
IoT
blockchain
python
C++
C
engage
digital
neural networks
Wireless
Algorithm
'''
train_df = []
keyword = {'security': 1, 'data': 2, 'software': 3, 'algorithm': 4, 'application': 5, 'network': 6,
           'distributed': 7, 'IoT': 8, 'blockchain': 9, 'python': 10, 'C++': 11, 'C': 12, 'engage': 13, 'digital': 14,
           'neural': 15, 'wireless': 16, 'search': 17, 'system': 18, 'vision': 19, 'hardware':20, 'compression':21, 'machine learning': 22}
for i in keyword:
    for j in description:
        count1 = 0
        m = description[j].split()
        for t in m:
            if i == t or i.capitalize() == t or (i+'s') == t:
                count1 += 1
        train_df.append([id[j], keyword[i], count1])
train_df = np.array(train_df)
rating = train_df
#print(train_df[:100])
user_similarity = cosine_similarity(train_df, dense_output=True)
#print(user_similarity)

def KNN(items, ratings, item_similarity, keywords, k):
    movie_list = []
    movie_id = items[keywords]
    #print(item_similarity)
    movie_similarity = item_similarity[movie_id - 1]
    #print(movie_similarity)
    movie_similarity_index = np.argsort(-movie_similarity)[1:k + 1]
    print(movie_similarity_index)
    for index in movie_similarity_index:
        for i in items.keys():
            if items[i] == ratings[index][0]:
                if i not in movie_list:
                    movie_list.append(i)
        #move_list.append(movie_similarity[index])
        #move_list.append(ratings[ratings['item_id'] == index + 1].rating.mean())
        # move_list.append(len(ratings[ratings['item_id'] == index + 1]))

    return movie_list
sim = {}
for course in id.keys():
    x = KNN(id,train_df,user_similarity,course,3)
    y = description[course].split()
    for t in y:
        if t in id.keys():
            if course not in x:
                x.append(t)
    for j in description:
        if course in description[j]:
            if course not in x:
                x.append(j)
    m = ''
    for i in x:
        m  = m + i + ' '
    sim[course] = m

#print(sim)

jsonData = json.dumps(sim)
fileObject = open('course_similarity.json', 'w')
fileObject.write(jsonData)
fileObject.close()


   #13269257716








