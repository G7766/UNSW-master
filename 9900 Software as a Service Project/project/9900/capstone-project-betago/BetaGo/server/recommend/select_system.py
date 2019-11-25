import json
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity


def loadFont():
    f = open("new_db.json", encoding='utf-8')
    f2 = open("stream.json", encoding='utf-8')
    setting = json.load(f)
    setting2 = json.load(f2)
    terms = {}
    pre = {}
    core = {}
    ADK = {}
    dis = {}
    prescribe = {}
    for i in setting:
        terms[i] = setting[i]['offering terms']
        pre[i] = setting[i]['prerequisites']
    for i in setting2:
        try:

            core[i] = setting2[i]['core courses list']
            ADK[i] = setting2[i]['ADK list']
            dis[i] = setting2[i]['disciplinary electives list']
            prescribe[i] = setting2[i]['prescribed electives list']
        except:
            pass
    return setting2,terms,pre,core,ADK,dis,prescribe

in1 = input()
in2 = input()
stream,terms,pre,core,ADK,dis,prescribe = loadFont()
def al1(in1,in2):
    if in1 == 'Database Systems':
        for i in core['COMPDS']:
            if pre[i] == 'No prerequisites':
if in1 == 'Database Systems' or in1 == "e-Commerce Systems" or in1 == "Internetworking":
    111











