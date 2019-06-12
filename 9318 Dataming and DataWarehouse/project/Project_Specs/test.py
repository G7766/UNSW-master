
import heapq
import numpy


init_state =[0.2,0.2,0.2,0.2,0.2]
T = [[7/15,3/15,3/15,0,2/15],
	 [2/15,4/15,7/15,0,2/15],
	 [4/15,7/15,2/15,0,2/15],
	 [2/7,2/7,2/7,1/7,1/7],
	 [1/4,1/4,1/4,1/4,1/4]
]
E = [[4/10,3/10,2/10,1/10],
	 [2/10,4/10,3/10,1/10],
	 [2/10,2/10,5/10,1/10],
	 [0,0,0,0],
	 [0,0,0,0]
]

state = ['S1','S2','S3','BEGIN','END']
symbol = ['RED','GREEN','BLUE','UNK']
pi = [0.2,0.2,0.2,0.2,0.2]

O = [0,0,1,2]


import numpy as np
def viterbi(trainsition_probability,emission_probability,pi,obs_seq):
	#转换为矩阵进行运算
	trainsition_probability=np.array(trainsition_probability)
	emission_probability=np.array(emission_probability)
	pi=np.array(pi)
	# 最后返回一个Row*Col的矩阵结果
	Row = np.array(trainsition_probability).shape[0]
	Col = len(obs_seq)
	#定义要返回的矩阵
	print(Col)
	print(Row)
	F=np.zeros((Row,Col))
	print(F)
	#初始状态
	F[:,0]=pi*np.transpose(emission_probability[:,obs_seq[0]])
	for t in range(1,Col):
		list_max=[]
		for n in range(Row):
			list_x=list(np.array(F[:,t-1])*np.transpose(trainsition_probability[:,n]))
			#获取最大概率
			list_p=[]
			for i in list_x:
				list_p.append(i*10000)
			list_max.append(max(list_p)/10000)
		F[:,t]=np.array(list_max)*np.transpose(emission_probability[:,obs_seq[t]])
	return F

result =viterbi(T,E,pi,O)
print(result)

#for i in len(result):
#	for j in len(result[0]):
#		
#for k in range(len(result)):
#	print(state[int(result[k])])



for i in range(1,4):
	print(i)
	
print(numpy.e)



l= {}
ll= dict(l)
l[1]=2
print(ll)

for k in range(2):
	print(k)
	
	
state = {'a':['aa','S1'],'b':'S2','c':'S3','d':'BEGIN','e':'END'}
for i in state:
	print(i+':',[z for z in state[i]])
	
	
z = [0.]* 3
print(z)


#for t in range(3,0,-1):
#	print(t)
	
for i in range(3,1,-1):
	print(i)
	
def kViterbiParallel(pi, a, b, obs, topK):
#	if topK == 1:
#		return viterbi(pi, a, b, obs)
#
	nStates = np.shape(b)[0]
	print('nStates:',nStates)
	T = np.shape(obs)[0]

#	assert (topK <= np.power(nStates, T)), "k < nStates ^ topK"

	# delta --> highest probability of any path that reaches point i
	delta = np.zeros((T, nStates, topK))
	print('delta:',delta)

	# phi --> argmax
	phi = np.zeros((T, nStates, topK), int)

	#The ranking of multiple paths through a state
	rank = np.zeros((T, nStates, topK), int)

	# for k in range(K):
	for i in range(nStates):
		delta[0, i, 0] = pi[i] * b[i][obs[0]]
		phi[0, i, 0] = i

		#Set the other options to 0 initially
		for k in range(1, topK):
			delta[0, i, k] = 0.0
			phi[0, i, k] = i

	#Go forward calculating top k scoring paths
	# for each state s1 from previous state s2 at time step t
	for t in range(1, T):
		for s1 in range(nStates):

			h = []

			for s2 in range(nStates):
				# y = np.sort(delta[t-1, s2, :] * a[s2, s1] * b[s1, obs[t]])

				for k in range(topK):
					prob = delta[t - 1][s2][k] * a[s2][s1] * b[s1][obs[t]]
					# y_arg = phi[t-1, s2, k]

					state = s2

					# Push the probability and state that led to it
					heapq.heappush(h, (prob, state))

			#Get the sorted list
			h_sorted = [heapq.heappop(h) for i in range(len(h))]
			h_sorted.reverse()

			#We need to keep a ranking if a path crosses a state more than once
			rankDict = dict()

			#Retain the top k scoring paths and their phi and rankings
			for k in range(0, topK):
				delta[t, s1, k] = h_sorted[k][0]
				phi[t, s1, k] = h_sorted[k][1]

				state = h_sorted[k][1]

				if state in rankDict:
					rankDict[state] = rankDict[state] + 1
				else:
					rankDict[state] = 0

				rank[t, s1, k] = rankDict[state]

	# Put all the last items on the stack
	h = []

	#Get all the topK from all the states
	for s1 in range(nStates):
		for k in range(topK):
			prob = delta[T - 1, s1, k]

			#Sort by the probability, but retain what state it came from and the k
			heapq.heappush(h, (prob, s1, k))

	#Then get sorted by the probability including its state and topK
	h_sorted = [heapq.heappop(h) for i in range(len(h))]
	h_sorted.reverse()

	# init blank path
	path = np.zeros((topK, T), int)
	path_probs = np.zeros((topK, T), float)

	#Now backtrace for k and each time step
	for k in range(topK):
		#The maximum probability and the state it came from
		max_prob = h_sorted[k][0]
		state = h_sorted[k][1]
		rankK = h_sorted[k][2]

		#Assign to output arrays
		path_probs[k][-1] = max_prob
		path[k][-1] = state

		#Then from t down to 0 store the correct sequence for t+1
		for t in range(T - 2, -1, -1):
			#The next state and its rank
			nextState = path[k][t+1]

			#Get the new state
			p = phi[t+1][nextState][rankK]

			#Pop into output array
			path[k][t] = p

			#Get the correct ranking for the next phi
			rankK = rank[t + 1][nextState][rankK]

	return path, path_probs, delta, phi
	


#init_state =[0.2,0.2,0.2,0.2,0.2]
T = [[7/15,3/15,3/15,0,2/15],
	 [2/15,4/15,7/15,0,2/15],
	 [4/15,7/15,2/15,0,2/15],
	 [2/7,2/7,2/7,1/7,1/7],
	 [1/4,1/4,1/4,1/4,1/4]
]
E = [[4/10,3/10,2/10,1/10],
	 [2/10,4/10,3/10,1/10],
	 [2/10,2/10,5/10,1/10],
	 [0,0,0,0],
	 [0,0,0,0]
]

state = ['S1','S2','S3','BEGIN','END']
symbol = ['RED','GREEN','BLUE','UNK']
pi = [2/7,2/7,2/7,1/7,1/7]

O = [0,3,2]

path, path_probs, delta, phi = kViterbiParallel(pi, T, E, O, 3)

print('@')
print(path)


z= [1,2,3,4,6]
l = z[1:-1]
print(l)

z = [1,2,3,4]

print(z[:2])