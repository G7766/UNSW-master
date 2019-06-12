#Author:Alexander Yang
# Import your files here...
import pandas as pd
import numpy as np
import re
import math
# Question 1
def viterbi_algorithm(State_File, Symbol_File, Query_File): # do not change the heading of the function
    pass


# Question 2
def top_k_viterbi(State_File, Symbol_File, Query_File, k): # do not change the heading of the function
    pass # Replace this line with your implementation...


# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File): # do not change the heading of the function
    pass # Replace this line with your implementation...


state_file='toy_example/State_File'
symbol_file='toy_example/Symbol_File'
query_file='toy_example/Query_File'
viterbi_result = viterbi_algorithm(state_file, symbol_file, query_file)
# processing data A in basic viterbi algorithm, here A equals state file
s1 = open(state_file,  encoding = 'utf-8')
N = int(s1.readline())
s2 = open(state_file,  encoding = 'utf-8')
next(s2)
stateList = [] # all state  list
for i in range(N):
    stateList.append(s2.readline().strip())
dataLine_A = next(s2)
list1_A = [] #define 3 list in orfer to transfer to the 2D matrix, the first column is the first index.....
list2_A = []
list3_A = []
while dataLine_A:
    a = dataLine_A.split()
    b = a[:1] #split the first data in all the  data line\
    c = a[1:2] #split the second column data in all the  data line
    d = a[2:3]  # split the third  column data in all the  data line
    list1_A.append(int(b[0]))
    list2_A.append(int(c[0]))
    list3_A.append(int(d[0]))
    dataLine_A = s2.readline()
#merge to 2D list representing state transition probablity matrix in basic viterbi algorithm
state_transition_frequency_matrix = [[0 for state_matrix_column in range(N)] for state_matrix_row  in range(N)]
#bind list1_A, list2_A, list3_A into state_transition_frequency_matrix
for i in range(len(list1_A)):
    index_A_1 = list1_A[i]
    index_A_2 = list2_A[i]
    state_transition_frequency_matrix[index_A_1][index_A_2] = list3_A[i]

#print(list1_A)
#print(list2_A)
#print(list3_A)
print('')
print('???',state_transition_frequency_matrix)
print('')
##
##
# processing data B in basic viterbi algorithm, here B equals symbol file
S1 = open(symbol_file,  encoding = 'utf-8')
M = int(S1.readline())
S2 = open(symbol_file,  encoding = 'utf-8')
next(S2)
symbolList = [] # all symbol  list
for i in range(M):
    symbolList.append(S2.readline().strip())
#print(symbolList)
dataLine_B = next(S2)
list1_B = [] #define 3 list in orfer to transfer to the 2D list, the first column is the first index.....
list2_B = []
list3_B = []
while dataLine_B:
    a = dataLine_B.split()
    b = a[:1] #split the first data in all the  data line
    c = a[1:2] #split the second column data in all the  data line
    d = a[2:3]  # split the third  column data in all the  data line
    list1_B.append(int(b[0]))
    list2_B.append(int(c[0]))
    list3_B.append(int(d[0]))
    dataLine_B = S2.readline()
#merge to 2D list representing emission transition frequency matrix in basic viterbi algorithm, for the prob, need to calculate and smooth further
emission_transition_frequency_matrix = [[0 for emission_matrix_column in range(M)] for emission_matrix_row  in range(N-2)] #state Begin and End cannot emit
#bind list1_B, list2_B, list3_B into emission_transition_frequency_matrix
for i in range(len(list1_B)):
    index_B_1 = list1_B[i]
    index_B_2 = list2_B[i]
    emission_transition_frequency_matrix[index_B_1][index_B_2] = list3_B[i]

'''
print(list1_B)
print(list2_B)
print(list3_B)
'''
#calculate pi
n = N - 2
pi=[]
ppppi=[]
print('state_transition_frequency_matrix[n]:',state_transition_frequency_matrix[n])
piSumFrequency = sum(state_transition_frequency_matrix[n]) + N - 1
print('piSumFrequency',piSumFrequency)
loopTimes_pi = len(state_transition_frequency_matrix[n])
for p in range(loopTimes_pi):
    ppppi.append((state_transition_frequency_matrix[n][p] + 1)/piSumFrequency)
    pi.append(math.log((state_transition_frequency_matrix[n][p] + 1)/piSumFrequency))
print('!!!',pi)
#print(2/7)
print('ppppi:',ppppi)
#
#
##calculate state to end
m = N - 1
end=[]
loopTimesEnd = len(state_transition_frequency_matrix)
print(loopTimesEnd)
for e in range(loopTimesEnd):
    endSumFrenquency = (sum(state_transition_frequency_matrix[e]) + N - 1)
    end.append((state_transition_frequency_matrix[e][m] + 1 )/endSumFrenquency )
print('end:',end)
#
#
#processing viterbi algorithm
q = open(query_file,  encoding = 'utf-8')
for eachLine in q:
    observation = re.split('([,|\(|\)|\/|\-|\&|\s])',eachLine)
    observation_new=[]
    for term in observation:
        if (term.isspace()==False and term !="\n" and term!=""):
           observation_new.append(term)
    print(observation_new)
    T = len(observation_new)
    delta = [[0 for i in range(n)] for t in range(T)]
    pre = [[0 for i in range(n)] for t in range(T)]
    B=[[0 for t in range(T)] for i in range(n)]
    position = observation_new.index(observation_new[0])
    #position_1 = observation_new.index(observation_new[T-1])
    for d in range(n):
        bSumFrenquency = sum(emission_transition_frequency_matrix[d]) + M + 1
        if (observation_new[0] in symbolList ):
            B[d][0] = math.log((emission_transition_frequency_matrix[d][position] + 1)/bSumFrenquency)
            delta[0][d] = pi[d] + B[d][0] + end[d]
        else:
            B[d][0] = math.log(1 / bSumFrenquency)
            delta[0][d] = pi[d] + B[d][0] + end[d]
    
    print('delta',delta)
    for t in range(1, T):
        for i in range(n):
            bSumFrenquency_1 = sum(emission_transition_frequency_matrix[i]) + M + 1
            delta[t][i] = delta[t - 1][0] + math.log((state_transition_frequency_matrix[0][i] + 1)/(sum(state_transition_frequency_matrix[0]) + N - 1))
            for j in range(1, n):
                vj = delta[t - 1][j] + math.log((state_transition_frequency_matrix[j][i] + 1)/(sum(state_transition_frequency_matrix[j]) + N - 1))
                if delta[t][i] < vj:
                    delta[t][i] = vj
                    pre[t][i] = j
                #print(pre)
            if (observation_new[t] in symbolList):
                B[i][t] = math.log((emission_transition_frequency_matrix[i][observation_new.index(observation_new[t])] + 1) / bSumFrenquency_1)
                delta[t][i] = delta[t][i] + B[i][t] + end[i]
            else:
                B[i][t] = math.log(1 / bSumFrenquency_1)
                delta[t][i] = delta[t][i] + B[i][t] + end[i]

    decode = [-1 for t in range(T)]
    print(decode)
    q = 0
    for i in range(1, n):
        if delta[T-1][i] > delta[T-1][q]:
            q = i
    decode[T-1] = q
    for t in range(T-2, -1, -1):
        '''
        for i in range(1, n):
            if delta[t][i] > delta[t][q]:
                q = i
        decode[t] = q
        '''
        q = pre[t+1][q]
        decode[t] = q
    print(decode)


'''
l=re.split('([,|\(|\)|\/|\-|\&|\s|])', '8/23-35 Barker St., Kingsford, NSW 2032')
#l=[x for x in l if x]
a = list(filter(, l))
print(a)
'''
'''
#print(list_Q[0])
splitTokens=nlp('8/23-35 Barker St., Kingsford, NSW 2032')
t=[]
t=[token.orth_ for token in splitTokens]
for term in t:
    if ('/' in term):
        x=term.split('/')
        y = t.index(term)
        t.remove(term)
        #print(t)
        x.insert(1,'/')
        for i in range(len(x)) :
            t.insert(y, x[i])
            i += 1

print(t)
'''
'''
for times in range(len(list_Q)):
    splitTokens = nlp(list_Q[times])
   #print([token.orth_ for token in splitTokens])
    print([token.orth_ for token in splitTokens if not token.is_punct | token.is_space])
'''


