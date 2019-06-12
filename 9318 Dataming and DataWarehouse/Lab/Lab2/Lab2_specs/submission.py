## import modules here 
import pandas as pd
import numpy as np



################# Question 1 #################


def get_sse(l):
    if len(l)==0:
        return 0.0
    # average of the list
    average = np.average(l)
    ll =[]
    for i in l:
        x = (i-average)*(i-average)
        ll.append(x)
    value = sum(ll)
    return value

def v_opt_dp2(x, b, matrix, matrix_list,matrix_list_best ,x_leave, bin_empty):
    if (x_leave == len(x)):
        #print('b')
        x_leave = 0
        bin_empty = bin_empty - 1
        if(bin_empty <0):
            return
        v_opt_dp2(x, b, matrix, matrix_list, matrix_list_best, x_leave, bin_empty)
    if bin_empty <=x_leave and (len(x) - x_leave) >= (b - bin_empty):
        rest_list = x[x_leave:]
        #print(rest_list)
        #print(bin_empty)
        #print(x_leave)
        if bin_empty == b-1:
            cost = get_sse(rest_list)
            matrix[0][x_leave] = cost
            matrix_list[0][x_leave]= [rest_list]
            matrix_list_best[0][x_leave] = [rest_list]
            v_opt_dp2(x, b, matrix, matrix_list,matrix_list_best ,x_leave + 1, bin_empty)
        else:
            currcostL = []
            pathL =[]
            if len(rest_list) == b - bin_empty:
                min_cost = 0
                for e in rest_list:
                    pathL.append([e])
            else:
                for h in range(1,len(rest_list)-(b-bin_empty)+2):
                    prefix = rest_list[:h]
                    suffix = rest_list[h:]
                    pre_cost = get_sse(prefix)
                    # serch the previous result as index
                    index = matrix_list[b-bin_empty-2].index([suffix])
                    # print('index:',index)
                    suf_path = matrix_list_best[b-bin_empty - 2][index]
                    suf_cost = matrix[b-bin_empty - 2][index]

                    cost = pre_cost + suf_cost
                    #print(cost)
                    currcostL.append(cost)

                    curr_path = [prefix] + suf_path
                    pathL.append(curr_path)
                # select the best result(min cost) to put in the matrix
                min_cost = min(currcostL)
                # put the min cost list into the best_matrix_list
                min_cost_index = currcostL.index(min_cost)
                pathL = pathL[min_cost_index]
            # record the best list into best_matrix_list
            #print('b',b)
            #print('bin_empty', bin_empty)
            #print('b-bin_empty', b-bin_empty)
            matrix_list_best[b-bin_empty - 1][x_leave] = pathL
            matrix[b-bin_empty - 1][x_leave] = min_cost
            matrix_list[b-bin_empty - 1][x_leave] = [rest_list]

            v_opt_dp2(x, b, matrix, matrix_list, matrix_list_best, x_leave+1, bin_empty)
    else:
        #print('z')
        v_opt_dp2(x, b, matrix, matrix_list, matrix_list_best, x_leave + 1, bin_empty)



def v_opt_dp(x, num_bins):# do not change the heading of the function
    #pass # **replace** this line with your code
    # record the best cost
    matrix = [[-1 for i in range(len(x))] for j in range(num_bins)]
    # record index
    matrix_list = [[0 for i in range(len(x))] for j in range(num_bins)]
    matrix_list_best = [[0 for i in range(len(x))] for j in range(num_bins)]
    x_leave = 0
    bin_empty = num_bins - 1
    v_opt_dp2(x, num_bins, matrix, matrix_list,matrix_list_best ,x_leave, bin_empty)
    bins = matrix_list_best[-1][0]
    return matrix,bins

