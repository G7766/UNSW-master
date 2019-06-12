import numpy as np
import pandas as pd

data_file='./asset/a'
raw_data = pd.read_csv(data_file, sep=',')
print(raw_data.head())
#print(raw_data.head()['Col1'])
labels=raw_data['Label'].values
data=np.stack((raw_data['Col1'].values,raw_data['Col2'].values), axis=-1)
## Fixed Parameters. Please do not change values of these parameters...
weights = np.zeros(3) # We compute the weight for the intercept as well...
num_epochs = 50000
learning_rate = 50e-5


print('labels:\n',labels)
print('data:\n',data)

coefficient = [4,1,1,-1]
row_Data=[0.8,0.3,0.2]
def predict(row_data,coefficient):
    result = coefficient[0]
    for i in range(len(row_data) -1 ):
    	result += coefficient[i+1] * row_data[i]
    return result



def predict1(row_data,coefficient):
    result = coefficient[0]
    for i in range(len(row_data) -1 ):
        result += coefficient[i+1] * row_data[i]
    #result : result here is h(theata), 
    #but we need to return Sigmoid result g(z) = 1/(1+e(index(-z)))
    result = 1/(1+np.exp(-result))
    return result

#print(predict(row_Data,coefficient))
#print(predict1(row_Data,coefficient))
#print(np.exp(2))


def logistic_regression(data, labels, weights, num_epochs, learning_rate):
    m, n = np.shape(data)  # m is total number of sample, n is number of column
    # theta = np.ones(n+1)
    n = n + 1
    theta = np.array(weights).reshape(n, 1)
    # print(weights)
    # print('theta:',theta)

    max_iterations = num_epochs  # num_epochs is max iterations
    alpha = learning_rate

    x0 = np.ones((m, 1))
    x = np.hstack((x0, data))
    # print(x)

    # y = labels
    y = np.array(labels).reshape(m, 1)

    # GradientDescent:
    for i in range(0, max_iterations):
        h = np.dot(x, theta)
        # print('h:',h)
        h = 1 / (1 + np.exp(-h))  # sigmoid
        diff = h - y  # compute the difference, loss function
        gardient = np.dot(np.transpose(x), diff)  # (hj-yj)xj
        theta = theta - alpha * gardient  # theta is changinf
    theta = np.transpose(theta)
    theta = theta[0]
    # print(type(theta))
    return theta


z = logistic_regression(data, labels, weights, num_epochs, learning_rate)
print('z:', z)