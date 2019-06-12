# Import your files here...
import numpy as np
import re
import heapq


# create HMM model, and set the default value
class HMM:
	def __init__(self,states,symbols):
		self._states = states
		self._symbols = symbols
		self._T = None
		self._E = None
		self._priors = None
		self.O = None
		
		
	def set_transactions(self,transactions):
		self._T = transactions
	
	def set_emissions(self, emissions):
		self._E = emissions
		
	def set_priors(self,init_state):
		self._priors = init_state
	def set_O(self,O):
		self.O = O




# viterbi_path, input the observation sequence and the hmm model
# in this function, most of value type i use are dict type
def viterbi_path(O, hmm):
	#Return most likely hidden state path given observation sequence O.
	n = len(O)

	u = {state: list() for state in hmm._states}

	v = {state: list() for state in hmm._states}
	bt = list()
	for o in O:
		for state in hmm._states:
			for t in (u, v):
				u[state].append(0)
				v[state].append(str())
		bt.append(str())

	for state in hmm._states:
		u[state][0] = hmm._priors[state] * hmm._E[state][O[0]]  # calculate the first obervation with initial state

#	print(u)
		# v[state][0] not of interest
	count = 0
	for t in range(1, n):
		for j in hmm._states:
			for i in hmm._states:
				p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]     # finding the largest value in every point
				if p > u[j][t]:
					u[j][t] = p
					v[j][t] = i

#	print('u:\n',u)
#	print('v:\n',v)
	
	p = 0 #retract and find the path
	for state in hmm._states:
		if u[state][n-1] > p:
			p = u[state][n-1]
			bt[n-1] = state
	
	
	for t in range(n-2, -1, -1):
		bt[t] = v[bt[t+1]][t+1]
	
	# state -> END
	#print('p',p)
	#print(bt[-1])
	p = np.log(p * (hmm._T[bt[-1]]['END']))        # calculate the last state to end state
	
	return bt, p
	

		
	
	
	
	
# This function is use for read state_file and symbol_file
def readSS_file(file):
	content = []
	z = 0
	_num = 0            # used for count state or symbol number
	with open(file) as f:
		for line in f:
			line = line.split()
			if z == 0:
				_num = int(line[0])
				line = [_num]
			if z>_num:
				l = []
				for i in line:
					l.append(int(i))
				line = l
			content.append(line)
			z +=1
		#print(content)
	return content

def readQuery_file(file):
	query_content = []
	with open(file) as f:
		for line in f:
			line = line.split()
			query_content.append(line)
		#print(query_content)
	return query_content


# This is for read Query_file, and parse the address as the question required
def ReadQuery_file(file):
	query_content = []
	with open(file) as f:
		for line in f:
			z = []
			line = re.split('([,\(\)\/\-\&\s])',line)
			for i in line:
				if i.isspace() == False and i!="\n" and i !="":
					z.append(i)
			query_content.append(z)
		#print(query_content)
	return query_content

# input the read file result and return the transaction_matrix
def create_transaction_matrix(content,q3=False):
	_num = content[0][0]
	state = []
	for i in range(1,_num+1):
		state.append(content[i][0])
#    print(state)

	state_index = {}
	z = 0
	for i in range(len(state)):
		state_index[i] = state[z]
		z +=1
	#print(state_index)
	
	transaction_matrix = {}
	for i in state:
		transaction_matrix[i]={}
		for j in state:
			transaction_matrix[i][j]=0
#    print(transaction_matrix[1][0])
	for i in range(_num+1,len(content)):
		transaction_matrix[state_index[content[i][0]]][state_index[content[i][1]]] = content[i][2]
	#print(transaction_matrix)
	
	if q3 == True:
		smooth = 1
		transaction_matrix[state_index[9]][state_index[19]] = transaction_matrix[state_index[9]][state_index[19]] + transaction_matrix[state_index[0]][state_index[19]]
		transaction_matrix[state_index[24]][state_index[9]] = transaction_matrix[state_index[24]][state_index[0]] + 10
		transaction_matrix[state_index[8]][state_index[1]] = transaction_matrix[state_index[8]][state_index[8]] -1 
	else:
		smooth = 1
#	kkk = 0 
#	for i in transaction_matrix:
#		print('k:',kkk,' ',transaction_matrix[i])
#		kkk= kkk+1

	#compute probability:
	for i in state:
		if i == 'END':
			continue
		sum_up = sum(transaction_matrix[i].values())+(len(state)*smooth) - 1
		for j in state:
			if transaction_matrix[i][j] == 0:
				if j == 'BEGIN':
					continue
				transaction_matrix[i][j] = smooth / sum_up 
			else:
				transaction_matrix[i][j] = (transaction_matrix[i][j] + smooth) / sum_up
		

	return transaction_matrix,state

		

# input the read file result and return the emission_matrix
def create_emission_matrix(content, state, q3=False):
	_num = content[0][0]    
	symbol = []
	
	for i in range(1,_num+1):
		symbol.append(content[i][0])
	symbol.append('UNK')   # the last one as UNK
	
	#print(symbol)
	
	state_index = {}
	z = 0
	for i in range(len(state)):
		state_index[i] = state[z]
		z +=1
	symbol_index = {}
	z = 0
	for i in range(len(symbol)):
		symbol_index[i] = symbol[z]
		z +=1
	#print(symbol_index)
	
	
	emission_matrix = {}
	for i in state:
		emission_matrix[i]={}
		for j in symbol:
			emission_matrix[i][j]=0
#    print(emission_matrix[1][0])
	for i in range(_num+1,len(content)):
		emission_matrix[state_index[content[i][0]]][symbol_index[content[i][1]]] = content[i][2]
	
	#print(emission_matrix)

	if q3 == True:
		smooth = 1
	else:
		smooth = 1
	#compute probability:
	z = 0
	for i in state:
		if i =='BEGIN' or i =='END':
			continue
		if z<len(state)-2:
			z +=1
			sum_up = sum(emission_matrix[i].values())+(len(symbol)-1)*smooth + 1 # len of state already add 1 as UNK
			for j in symbol:
				if emission_matrix[i][j] == 0:
					emission_matrix[i][j] = smooth / sum_up
				else:
					emission_matrix[i][j] = (emission_matrix[i][j] + smooth) / sum_up
	return emission_matrix, symbol




# for Q2, i have tought using the function viterbi_path, but i feel that it is more easy to use np.array type
# so In Q2 i change the dict type to np.array and input the relative transaction array and observation array
# and input initial state rate pi, and topK
def TOP_KViterbi(pi, a, b, obs, topK):
	nStates = np.shape(b)[0]
	#print('nStates:',nStates)
	T = np.shape(obs)[0]
	


	# delta  to restore the highest probability of any path that reaches point i
	delta = np.zeros((T, nStates, topK))
	#print('delta:\n',delta)

	# phi to restore the argmax
	phi = np.zeros((T, nStates, topK), int)
	#print('phi:\n',phi)
	#The ranking of multiple paths through a state
	rank = np.zeros((T, nStates, topK), int)
	#print('rank:\n',rank)
	
	#print(pi)
	# for k in range(K):
	for i in range(nStates):
		delta[0, i, 0] = pi[i] * b[i][obs[0]]
		phi[0, i, 0] = i

		#Set the other options to 0 initially
		for k in range(1, topK):
			delta[0, i, k] = 0.0
			phi[0, i, k] = i
	
#	print('delta:\n',delta)
	#print('phi:\n',phi)
	#Go forward calculating top k scoring paths
	# for each state s1 from previous state s2 at time step t
	for t in range(1, T):
		for s1 in range(nStates):
			h = []
			for s2 in range(nStates):
				for k in range(topK):
					prob = delta[t - 1][s2][k] * a[s2][s1] * b[s1][obs[t]]
					state = s2
					# Push the probability and state that led to it
					heapq.heappush(h, (prob, state))

			#Get the sorted list
			h_sorted = [heapq.heappop(h) for i in range(len(h))]
			h_sorted.reverse()


			#It need to keep a ranking if a path crosses a state more than once
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
	
#	print('delta:\n',delta)
#	print('phi:\n',phi)
	#Get all the topK from all the states
	for s1 in range(nStates):
		for k in range(topK):
			prob = delta[T - 1, s1, k]

			#Sort by the probability, but retain what state it came from and the k
			heapq.heappush(h, (prob, s1, k))
			#print('h:',h)

	#Then get sorted by the probability including its state and topK
	h_sorted = [heapq.heappop(h) for i in range(len(h))]
	h_sorted.reverse()
#	print(h_sorted)

	# init blank path
	path = np.zeros((topK, T), int)
	path_probs = np.zeros((topK, T), float)

	#Now backtrace for k and each time step

	count = 0
	for i in range(len(h_sorted)-1):
		if topK == 1 or topK >= len(h_sorted):
			break
		else:
			if h_sorted[i][0]!=h_sorted[i+1][0]:
				#print(i)
				count +=1
				if count == topK:
					num = i
					break
#	print('num:',num)
			
			
			
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
	# to deal with the tipe, it needs to return the top top//2 result, 
	#so that the result will be in order
	
	#print(topK)
	path = path[:topK//2]
	

	return path

# to calculate the path log probability
def calculate_log(path,a,b,obs):
	p = 1
	l = path[1:-1]
	#print(len(path))
	#print(len(l))
	#print(len(obs))
	for i in range(len(l)):
		p = p * b[l[i]][obs[i]]
	
	for i in range(len(path)-1):
		p = p * a[path[i]][path[i+1]]
	
	p = np.log(p)
			
	return p
	


#Q1 Finding the best path of the viterbi_algorithm 
def viterbi_algorithm(State_File, Symbol_File, Query_File): # do not change the heading of the function
#	pass # Replace this line with your implementation...
	State_content = readSS_file(State_File)
	transaction_matrix, state = create_transaction_matrix(State_content)
	#print('transaction_matrix:\n',transaction_matrix)
#	print('')
	Symbol_content = readSS_file(Symbol_File)

	emission_matrix, symbol = create_emission_matrix(Symbol_content, state)
#	print('')
	#print('emission_matrix:\n',emission_matrix)
#
#	print('')
	query_content = ReadQuery_file(Query_File)
	#print(symbol)



	model = HMM(state,symbol)
	#model = HMM([0,1,2,3,4],[0,1,2,3])
	model.set_transactions(transaction_matrix)
	model.set_emissions(emission_matrix)

	init_state = transaction_matrix['BEGIN']
	#init_state = {'S1': 0.2, 'S2': 0.2, 'S3': 0.2, 'BEGIN': 0.2, 'END': 0.2}  wrong

	#print(init_state)
	#print(init_state)
	model.set_priors(init_state)
	#print('')


	#a = ['Red','Red','Green','Blue']
	final_result = []
	for row in query_content:
		for i in range(len(row)):
			if row[i] not in symbol:
				row[i] = 'UNK'
		aa = []
		aa.append(state.index('BEGIN'))
		result,p = viterbi_path(row,model)
		for i in result:
			aa.append(state.index(i))
		aa.append(state.index('END'))
		aa.append(p)
		final_result.append(aa)
	
	return final_result
			





# Question 2

def top_k_viterbi(State_File, Symbol_File, Query_File, k): # do not change the heading of the function
#	pass # Replace this line with your implementation...
	State_content = readSS_file(State_File)
	transaction_matrix, state = create_transaction_matrix(State_content)
	Symbol_content = readSS_file(Symbol_File)
	emission_matrix, symbol = create_emission_matrix(Symbol_content, state)
	query_content = ReadQuery_file(Query_File)

	model = HMM(state,symbol)

	model.set_transactions(transaction_matrix)
	model.set_emissions(emission_matrix)

	init_state = transaction_matrix['BEGIN']

	model.set_priors(init_state)
	
	# change the dict to np.array
	a = [[] for _ in range(len(model._states))]
	b = [[] for _ in range(len(model._states))]
	count = 0
	for i in model._states:
		for j in model._states:
			a[count].append(transaction_matrix[i][j])
		count+=1
	#print(a)
	count = 0
	for i in model._states:
		for j in model._symbols:
			b[count].append(emission_matrix[i][j])
		count+=1
	#print(b)
	
	pi = []
	for i in init_state:
		pi.append(init_state[i])
	#print(pi)
	
	topK = 2*k

	
	#TOP_KViterbi(pi, a, b, obs, topK)
	#a = ['Red','Red','Green','Blue']
	final_path = []
	final_result = []
	for row in query_content:
		for i in range(len(row)):
			if row[i] not in symbol:
				row[i] = 'UNK'
		obs = []
		for i in row:
			obs.append(symbol.index(i))
		#print(obs)
		path = TOP_KViterbi(pi, a, b, obs, topK)
		for i in path:
			i = i.tolist()
			i.insert(0,state.index('BEGIN'))
			i.append(state.index('END'))
			ln_probability = calculate_log(i,a,b,obs)
			i.append(ln_probability)
			final_path.append(i)
	return final_path




# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File): # do not change the heading of the function
#	pass # Replace this line with your implementation...
	#	pass # Replace this line with your implementation...
		State_content = readSS_file(State_File)
		#This is Q3, so we need to change the transaction_matrix a little 
		transaction_matrix, state = create_transaction_matrix(State_content,True)
#		print('transaction_matrix:\n',transaction_matrix)

		Symbol_content = readSS_file(Symbol_File)
		
		#This is Q3, so we need to change the emission_matrix a little 
		emission_matrix, symbol = create_emission_matrix(Symbol_content, state,True)

#		print('emission_matrix:\n',emission_matrix)

#		print('emission_matrix:')

		query_content = ReadQuery_file(Query_File)
		#print(symbol)


		model = HMM(state,symbol)
		#model = HMM([0,1,2,3,4],[0,1,2,3])
		model.set_transactions(transaction_matrix)
		model.set_emissions(emission_matrix)

		init_state = transaction_matrix['BEGIN']
		#init_state = {'S1': 0.2, 'S2': 0.2, 'S3': 0.2, 'BEGIN': 0.2, 'END': 0.2}  wrong

		#print(init_state)
		model.set_priors(init_state)
		#print('')
		
		
		a = [[] for _ in range(len(model._states))]
		b = [[] for _ in range(len(model._states))]
		count = 0
		for i in model._states:
			for j in model._states:
				a[count].append(transaction_matrix[i][j])
			count+=1
		#print(a)
		count = 0
		for i in model._states:
			for j in model._symbols:
				b[count].append(emission_matrix[i][j])
			count+=1
		
			

		#a = ['Red','Red','Green','Blue']
		final_result = []
		#count_UNK = 0
		for row in query_content:
			for i in range(len(row)):
				if row[i] not in symbol:
					row[i] = 'UNK'
					#count_UNK +=1
			aa = []
			aa.append(state.index('BEGIN'))
			result,p = viterbi_path(row,model)
			for i in result:
				aa.append(state.index(i))
			aa.append(state.index('END'))
			aa.append(p)
			final_result.append(aa)
		#print('count_UNK:',count_UNK)
		
		return final_result

	


# test:
	
#State_File = 'toy_example/State_File'
#Symbol_File = 'toy_example/Symbol_File'
#Query_File ='toy_example/Query_File'
#

#State_File = 'dev_set/State_File'
#Symbol_File = 'dev_set/Symbol_File'
#Query_File ='dev_set/Query_File'
#result = top_k_viterbi(State_File, Symbol_File, Query_File, 5)
#for i in result:
#	print(i)
#
#query_label = ReadQuery_file(Query_Label)
#for i in range(len(result)):
#	result[i].pop()
#
#for i in result:
#	print(i)
#
#for i in range(len(query_label)):
#	for j in range(len(query_label[i])):
#		query_label[i][j] = int(query_label[i][j])
#
#
#count = 0
#for i in range(len(result)):
#	for j in range(len(result[i])):
#		if result[i][j]!= query_label[i][j]:
#			count+=1
#
#
#print('count:',count)