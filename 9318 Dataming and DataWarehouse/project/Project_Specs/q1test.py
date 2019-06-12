# Import your files here...
import numpy as np
import re
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
		u[state][0] = hmm._priors[state] * hmm._E[state][O[0]]

#	print(u)
		# v[state][0] not of interest
	count = 0
	for t in range(1, n):
		for j in hmm._states:
			for i in hmm._states:
				p = u[i][t-1] * hmm._T[i][j] * hmm._E[j][O[t]]
				if p > u[j][t]:
					u[j][t] = p
					v[j][t] = i

#	print('u:\n',u)
#	print('v:\n',v)
	
	p = 0
	for state in hmm._states:
		if u[state][n-1] > p:
			p = u[state][n-1]
			bt[n-1] = state
	
	
	for t in range(n-2, -1, -1):
		bt[t] = v[bt[t+1]][t+1]
	
	# state -> END
	#print('p',p)
	#print(bt[-1])
	p = np.log(p * (hmm._T[bt[-1]]['END']))
	
	return bt, p
	

		
	
	
	
	
	
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



#State_content = readSS_file('toy_example/State_File')
#transaction_matrix, state = create_transaction_matrix(State_content)
#print('transaction_matrix:\n',transaction_matrix)
#print('')
#Symbol_content = readSS_file('toy_example/Symbol_File')
#
#emission_matrix, symbol = create_emission_matrix(Symbol_content, state)
#print('')
#print('emission_matrix:\n',emission_matrix)
#
#print('')
#query_content = ReadQuery_file('toy_example/Query_File')
#
#
#
#
#model = HMM(state,symbol)
##model = HMM([0,1,2,3,4],[0,1,2,3])
#model.set_transactions(transaction_matrix)
#model.set_emissions(emission_matrix)
#
#init_state = transaction_matrix['BEGIN']
##init_state = {'S1': 0.2, 'S2': 0.2, 'S3': 0.2, 'BEGIN': 0.2, 'END': 0.2}
#
#
#print(init_state)
#model.set_priors(init_state)
#print('')
#
#
#a = ['Red','Red','Green','Blue']
#result,p = viterbi_path(a,model)
#print(result,p)
#
#b = ['Red','UNK','Blue']
#result,p = viterbi_path(b,model)
#print(result,p)






def viterbi_algorithm(State_File, Symbol_File, Query_File): # do not change the heading of the function
#	pass # Replace this line with your implementation...
	State_content = readSS_file(State_File)
	transaction_matrix, state = create_transaction_matrix(State_content)
	print('transaction_matrix:\n',transaction_matrix)
#	print('')
	Symbol_content = readSS_file(Symbol_File)

	emission_matrix, symbol = create_emission_matrix(Symbol_content, state)
#	print('')
#	print('emission_matrix:\n',emission_matrix)
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
			
		#print(result,p)

#	b = ['Red','UNK','Blue']
#	result,p = viterbi_path(b,model)
#	print(result,p)


#State_content = readSS_file('toy_example/State_File')
#transaction_matrix, state = create_transaction_matrix(State_content)
#print('transaction_matrix:\n',transaction_matrix)
#print('')
#Symbol_content = readSS_file('toy_example/Symbol_File')
#
#emission_matrix, symbol = create_emission_matrix(Symbol_content, state)
#print('')
#print('emission_matrix:\n',emission_matrix)
#
#print('')
#query_content = ReadQuery_file('toy_example/Query_File')


State_File = 'toy_example/State_File'
Symbol_File = 'toy_example/Symbol_File'
Query_File ='toy_example/Query_File'
#dev_set/

##Q1_final
#State_File = 'dev_set/State_File'
#Symbol_File = 'dev_set/Symbol_File'
#Query_File ='dev_set/Query_File'
#
viterbi_result = viterbi_algorithm(State_File, Symbol_File, Query_File)
for i in viterbi_result:
	print(i)






# Question 2







def top_k_viterbi(State_File, Symbol_File, Query_File, k): # do not change the heading of the function
	pass # Replace this line with your implementation...


# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File): # do not change the heading of the function
	pass # Replace this line with your implementation...
