# Import your files here...

# Question 1
class HMM:
    def __init__(self,states,symbols):
        self._states = states
        self._symbols = symbols
        self._T = None
        self._E = None
        self._priors = None
        
        
    def set_transactions(self,transactions):
        self._T = transactions
    
    def set_emissions(self, emissions):
        self._E = emissions
        
    def set_priors(self,init_state):
        self._priors = init_state
    
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
        # v[state][0] not of interest
    for t in range(1, n):
        for j in hmm._states:
            for i in hmm._states:
                p = u[i][t-1] * hmm._T[j][i] * hmm._E[j][O[t]]
                if p > u[j][t]:
                    u[j][t] = p
                    v[j][t] = i
    p = 0
    for state in hmm._states:
        if u[state][n-1] > p:
            p = u[state][n-1]
            bt[n-1] = state
    print(p)
    for t in range(n-2, -1, -1):
        bt[t] = v[bt[t+1]][t+1]

    return bt
    

    
    
    
    
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
        print(content)
    return content

def readQuery_file(file):
    query_content = []
    with open(file) as f:
        for line in f:
            line = line.split()
            query_content.append(line)
        print(query_content)
    return query_content

    
def create_transaction_matrix(content):
    _num = content[0][0]
    state = []
    for i in range(1,_num+1):
        state.append(content[i][0])
#    print(state)
    
    transaction_matrix = {}
    for i in range(len(state)):
        transaction_matrix[i]={}
        for j in range(len(state)):
            transaction_matrix[i][j]=0
#    print(transaction_matrix[1][0])
    for i in range(_num+1,len(content)):
        transaction_matrix[content[i][0]][content[i][1]] = content[i][2]
    
    #compute probability:
    for i in range(len(state)):
        sum_up = sum(transaction_matrix[i].values())+len(state) - 1
        for j in range(len(state)):
            if transaction_matrix[i][j] == 0:
                transaction_matrix[i][j] = 1 / sum_up 
            else:
                transaction_matrix[i][j] = (transaction_matrix[i][j] + 1) / sum_up
    print('transaction_matrix:')
    print(transaction_matrix)
    print('------------------')
    return transaction_matrix,state
        


def create_emission_matrix(content, state):
    _num = content[0][0]    
    symbol = []
    for i in range(1,_num+1):
        symbol.append(content[i][0])
    symbol.append('UNK')   # the last one as UNK
    print(symbol)
    print(state)
    
    emission_matrix = {}
    for i in range(len(state)):
        emission_matrix[i]={}
        for j in range(len(symbol)):
            emission_matrix[i][j]=0
#    print(emission_matrix[1][0])
    for i in range(_num+1,len(content)):
        emission_matrix[content[i][0]][content[i][1]] = content[i][2]
    
    #print(emission_matrix)
    
    #compute probability:
    for i in range(len(state)-2):
        sum_up = sum(emission_matrix[i].values())+len(symbol) # len of state already add 1 as UNK
        for j in range(len(symbol)):
            if emission_matrix[i][j] == 0:
                emission_matrix[i][j] = 1 / sum_up
            else:
                emission_matrix[i][j] = (emission_matrix[i][j] + 1) / sum_up
    for i in range(len(state)-2,len(state)):
        for j in range(len(symbol)):
            if emission_matrix[i][j] == 0:
                emission_matrix[i][j] = 1 / len(symbol)
    
    print('emission_matrix:')
    print(emission_matrix)
    print('------------------')
    return emission_matrix, symbol



State_content = readSS_file('toy_example/State_File')
transaction_matrix, state = create_transaction_matrix(State_content)
Symbol_content = readSS_file('toy_example/Symbol_File')
emission_matrix, symbol = create_emission_matrix(Symbol_content, state)

query_content = readQuery_file('toy_example/Query_File')




#model = HMM(state,symbol)
model = HMM([0,1,2,3,4],[0,1,2,3])
model.set_transactions(transaction_matrix)
model.set_emissions(emission_matrix)

# set initial state
init_state ={}
for i in range(len(state)):
    init_state[i]= 1/len(state)

print(init_state)
model.set_priors(init_state)



a = [0,0,1,2]
result = viterbi_path(a,model)
print(result)
b = [0,3,2] 
result = viterbi_path(b,model)
print(result)



def viterbi_algorithm(State_File, Symbol_File, Query_File): # do not change the heading of the function
    pass # Replace this line with your implementation...


# Question 2
def top_k_viterbi(State_File, Symbol_File, Query_File, k): # do not change the heading of the function
    pass # Replace this line with your implementation...


# Question 3 + Bonus
def advanced_decoding(State_File, Symbol_File, Query_File): # do not change the heading of the function
    pass # Replace this line with your implementation...
