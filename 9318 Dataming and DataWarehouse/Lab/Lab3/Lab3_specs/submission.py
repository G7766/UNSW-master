import pandas as pd
import numpy as np
def logistic_regression(data, labels, weights, num_epochs, learning_rate):# do not change the heading of the function
    #pass # **replace** this line with your code


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


