# Import your files here...
import numpy as np
# Question 1
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
	
def viterbi_path(O, hmm):
	"""Return most likely hidden state path given observation sequence O.
	"""
	n = len(O)
	for i in range(len(O)):
		if O[i] not in hmm._symbols:
			O[i] = 'UNK'

	u = {state: list() for state in hmm._states}
	uu = {state: list() for state in hmm._states}
	v = {state: list() for state in hmm._states}
	vv = {state: list() for state in hmm._states}
	bt = list()
	for o in O:
		for state in hmm._states:
			for t in (u, v):
				u[state].append(0)
				uu[state].append(0)
				v[state].append(str())
				vv[state].append([])
		bt.append(str())
	print(vv)
	
	for state in hmm._states:
		u[state][0] = hmm._priors[state] * hmm._E[state][O[0]]
		uu[state][0] = hmm._priors[state] * hmm._E[state][O[0]]
#	print(u)
		# v[state][0] not of interest

	for t in range(1, n):
		for j in hmm._states:
			last_record = {}
			for i in hmm._states:
				p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]
				last_record[i] = p
				if p > u[j][t]:
					u[j][t] = p
					v[j][t] = i
					vv[j][t] = [i]
			uu[j][t] = last_record
			for i in hmm._states:
				p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]
				if p == u[j][t] and i!= v[j][t]:
					vv[j][t].append(i)
	print('-------------------------')
	print('uu:')
	print_dict(uu)
	print('')
	print('vv:')
	print_dict(vv)
	# print('vv:')
	# print(vv)
	vv = {'S1': [[], ['S1'], ['S1'], ['S1'], [], [], [], []],
		  'S2': [[], ['S3'], ['S1'], ['S1'], [], [], [], []],
		  'S3': [[], ['S2'], ['S1'], ['S2'], [], [], [], []],
		  'BEGIN': [[], ['S1', 'S2', 'S3', 'BEGIN', 'END'], ['S1', 'S2', 'S3', 'BEGIN', 'END'], ['S1', 'S2', 'S3', 'BEGIN', 'END'], [], [], [], []],
		  'END': [[], ['S1', 'S2', 'S3', 'BEGIN', 'END'], ['S1', 'S2', 'S3', 'BEGIN', 'END'], ['S1', 'S2', 'S3', 'BEGIN', 'END'], [], [], [], []]}

	
	
#				if t!=n-1:
#					print(u[i][t-1],hmm._T[i][j],hmm._E[j][O[t]])
#					p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]
#					print(p)
#				else:
#					p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]
#					print(p)
#				if p > u[j][t]:
#					u[j][t] = p
#					v[j][t] = i
#					print('pick:', i )

#	print('u:\n',u)
#	print('v:\n',v)
	k = 4
	bbtt = list()
	path = list()
	for i in range(k):
		bbtt.append(list())
		path.append(list())
		for j in range(len(O)):
			bbtt[i].append('')
			path[i].append('')

	print('')
	print('bbtt:',bbtt)

	#print(path)
		
	
	l = []
	count = 0
	for m in range(k):
		p = 0
		for i_state in hmm._states:
			for j_state in hmm._states:
				if uu[i_state][n-1][j_state] > p:
#					print('!')
					p = uu[i_state][n-1][j_state]
					bbtt[m][n-1] = j_state
					z1 = j_state
					z2 = i_state
		l.append([z1,z2])
		uu[z2][n-1][z1] = 0
		print('l:',l)


		from_state = z1
		to_state = z2
		#print(z1,z2)
		print('~~~~~!!!!!!!:',path)
		path,count = recurse_find_path(path,count,k,from_state,to_state,uu,vv,n)
		print('!!',count)

		if count == k:
			break



#			for t in range(n-2, -1, -1):
#				bbtt[k][t] = v[bt[t+1]][t+1]
		
		 

#	for state in hmm._states:
#		if u[state][n-1] > p:
#			p = u[state][n-1]
#			bt[n-1] = state
#	print('p',p)
#	p = np.log(p * (1/len(hmm._states)))
#	for t in range(n-2, -1, -1):
#		bt[t] = v[bt[t+1]][t+1]
#	
#	print('u:',u)

	# Q2
#	top_k = []
##	uu = dict(u) 
#	k=2
#	pp = 0
#	for j in range(k):
#		print(bbtt)
#		z = []
#		for state in hmm._states:
#			if uu[state][n-1] > pp:
#				pp = uu[state][n-1]
#				bbtt[n-1] = state
#		#print('p',p)
#		print('pp:',pp)
#		pp = np.log(pp * (1/len(hmm._states)))
#		for t in range(n-2, -1, -1):
#			bbtt[t] = v[bbtt[t+1]][t+1]
#		for j in bbtt:
#			z.append(j)
#		print('bbtt:',bbtt)
#		top_k.append([z,pp])
#		print('top_k:',top_k)
#		uu[bbtt[-1]][n-1] = 0
#		pp = 0
#	print('uu:\n',uu)

	return #bt, p


def recurse_find_path(path,count,k,from_state,to_state,uu,vv,n):
	print('n:',n,'count:',count,'k:',k)
	print(from_state,to_state)
	print('?',path)
	if count == k:
		print('t1')
		return path,count
	if n==2:
		path[count][n-1] = to_state
		path[count][n-2] = from_state
		count+=1
		print(path)
		print('@@@')

		return path,count
	else:
		path[count][n-1] = to_state
		z = from_state
		to_state = from_state
		for i in vv[from_state][n-2]:
			from_state = i
			path,count = recurse_find_path(path,count,k,from_state,to_state,uu,vv,n-1)
			to_state = z
	return path,count


		
	
def print_dict(dict):
	for i in dict:
		print(i+':',[z for z in dict[i]],'\n')
	return
		
	
	
	
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

	
def create_transaction_matrix(content):
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
	
	#compute probability:
	for i in state:
		sum_up = sum(transaction_matrix[i].values())+len(state) - 1
		for j in state:
			if transaction_matrix[i][j] == 0:
				transaction_matrix[i][j] = 1 / sum_up 
			else:
				transaction_matrix[i][j] = (transaction_matrix[i][j] + 1) / sum_up
		

	return transaction_matrix,state
		


def create_emission_matrix(content, state):
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
	
	#compute probability:
	z = 0
	for i in state:
		if z<len(state)-2:
			z +=1
			sum_up = sum(emission_matrix[i].values())+len(symbol) # len of state already add 1 as UNK
			for j in symbol:
				if emission_matrix[i][j] == 0:
					emission_matrix[i][j] = 1 / sum_up
				else:
					emission_matrix[i][j] = (emission_matrix[i][j] + 1) / sum_up
#		else:
#			for j in symbol:
#				if emission_matrix[i][j] == 0:
#					emission_matrix[i][j] = 1 / sum_up

	
#	#print(emission_matrix)
#	
#	#emission_matrix_t
#	emission_matrix_t = {}
#	for i in symbol:
#		emission_matrix_t[i]={}
#		for j in state:
#			emission_matrix_t[i][j]=0
#
#	for i in range(_num+1,len(content)):
#		emission_matrix_t[symbol_index[content[i][1]]][state_index[content[i][0]]] = content[i][2]
#
#	
#	for i in symbol:
#		for j in state:
#			emission_matrix_t[i][j] = emission_matrix[j][i]
	
	return emission_matrix, symbol



def top_k_Viterbi(O,topK,hmm):
	"""
	Return most likely hidden state path given observation sequence O.
	"""
	n = len(O)
	delta = []
	phy = []
	for i in range(len(O)):
		delta.append({})
		phy.append({})

	t = 0
	o1 = O[t]
	curr_list = hmm._states    #returns all possible hidden states related to first element
	print(o1)
	for i in curr_list:
		delta[t][i] = [0.] * topK
		delta[t][i][0] = hmm._priors[i] * hmm._E[i][o1]
		phy[t][i] = [[0, 0, delta[t][i][0]]] * topK

	last_list = curr_list
	for t in range(1,n):
		o_t = O[t]
		for i in hmm._states:
			tmp = []
			for j in hmm._states:
				for d in range(topK):
					P = delta[t-1][j][d] * hmm._T[j][i] * hmm._E[i][o_t]
					tmp.append([P,j,i,P])
			tmp = sorted(tmp,key=lambda element: element[0], reverse = True)
			#print(tmp)

			delta[t][i] = list(map(lambda element: element[0], tmp)) + [0.] * topK
			phy[t][i] = list(map(lambda element: [element[1], element[2], element[3]], tmp)) + [[-1, -1]] * topK
			#print('phy[t][i]:',phy[t][i])
			delta[t][i] = delta[t][i][0: topK]
			phy[t][i] = phy[t][i][0: topK]
		last_list = curr_list

	result_1 =[]
	for i in delta[-1]:
		for d in range(topK):
			result_1.append([delta[-1][i][d], i, d])
			#print('result_1:',result_1)
	result_1 = sorted(result_1, key=lambda element: element[0], reverse=True)
	result_1 = result_1[0: topK]
	# print('')
	# print('delta:',delta,'\n')
	print('result_1:',result_1,'\n')
	print('phy:',phy,'\n')

	result = []
	for p, i, d in result_1:
		result.append([p])
		if p <= 0.:
			continue
#		print('p:',p,'i:',i,'d:',d)
		k = [i]
		current_i = i
		current_d = d
		print('p:',p,'current_i:',current_i,'current_d:',current_d)
		for t in range(n-1,0,-1):
			next_i, next_d, P = phy[t][current_i][current_d]
			k.append(next_i)
			current_i = next_i
			current_d = next_d

		k.reverse()
		result[d].append(k)
	return result
def recurse_find_path1(path,count,k,from_state,to_state,p,phy,n,T):
	if n != 0:
		for i in phy[n-2][from_state]:
			print('a')
			if (p/T[i[0]][i[1]]) == i[-1]:
				print('ok')
				return path, count
				from_state = i[0]
				p = p/T[from_state][to_state]
				path,count = recurse_find_path1(path,count,k,from_state,to_state,p,phy,n-1,T)
				p = p * T[from_state][to_state]
				to_state = z
	return path,count
		
		
	
	
#	n = len(O)
#
#	u = {state: list() for state in hmm._states}
#
#	v = {state: list() for state in hmm._states}
#	bt = list()
#	for o in O:
#		for state in hmm._states:
#			for t in (u, v):
#				u[state].append(0)
#				v[state].append(str())
#		bt.append(str())
#
#	for state in hmm._states:
#		u[state][0] = hmm._priors[state] * hmm._E[state][O[0]]
#
##	print(u)
#		# v[state][0] not of interest
#	count = 0
#	for t in range(1, n):
#		for j in hmm._states:
#			for i in hmm._states:
#				p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]
#				if p > u[j][t]:
#					u[j][t] = p
#					v[j][t] = i
#
##	print('u:\n',u)
##	print('v:\n',v)
#	
#	p = 0
#	for state in hmm._states:
#		if u[state][n-1] > p:
#			p = u[state][n-1]
#			bt[n-1] = state
#	
#	
#	for t in range(n-2, -1, -1):
#		bt[t] = v[bt[t+1]][t+1]
#	
#	# state -> END
#	#print('p',p)
#	#print(bt[-1])
#	p = np.log(p * (hmm._T[bt[-1]]['END']))
	
	return #bt, p

def kViterbiParallel(pi, a, b, obs, topK):
#	if topK == 1:
#		return viterbi(pi, a, b, obs)
#
	nStates = np.shape(b)[0]
	T = np.shape(obs)[0]

#	assert (topK <= np.power(nStates, T)), "k < nStates ^ topK"

	# delta --> highest probability of any path that reaches point i
	delta = np.zeros((T, nStates, topK))

	# phi --> argmax
	phi = np.zeros((T, nStates, topK), int)

	#The ranking of multiple paths through a state
	rank = np.zeros((T, nStates, topK), int)

	# for k in range(K):
	for i in range(nStates):
		delta[0, i, 0] = pi[i] * b[i, obs[0]]
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
					prob = delta[t - 1, s2, k] * a[s2, s1] * b[s1, obs[t]]
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





State_content = readSS_file('toy_example/State_File')
transaction_matrix, state = create_transaction_matrix(State_content)
print(transaction_matrix)
print('')
Symbol_content = readSS_file('toy_example/Symbol_File')

emission_matrix, symbol = create_emission_matrix(Symbol_content, state)
print('')
print(emission_matrix)

print('')
query_content = readQuery_file('toy_example/Query_File')




model = HMM(state,symbol)
#model = HMM([0,1,2,3,4],[0,1,2,3])
model.set_transactions(transaction_matrix)
model.set_emissions(emission_matrix)

init_state = {'S1': 0.2, 'S2': 0.2, 'S3': 0.2, 'BEGIN': 0.2, 'END': 0.2}


print(init_state)
model.set_priors(init_state)
print('')


a = ['Red','Red','Green','Blue']
b = ['Red','UNK','Blue']
#viterbi_path(b,model)
#print(result,p)


print('================')

#result = top_k_Viterbi(b,3,model)
print(result)





def viterbi_algorithm(State_File, Symbol_File, Query_File): # do not change the heading of the function
	pass # Replace this line with your implementation...












# Question 2







def top_k_viterbi(State_File, Symbol_File, Query_File, k): # do not change the heading of the function
	pass # Replace this line with your implementation...


# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File): # do not change the heading of the function
	pass # Replace this line with your implementation...
