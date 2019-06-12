def get_sse(l):
    if len(l) == 0:
        return 0.0
    # average of the list
    average = np.average(l)
    ll = []
    for i in l:
        x = (i - average) * (i - average)
        ll.append(x)
    value = sum(ll)
    return value


def v_opt_dp(x, b):  # do not change the heading of the function
    # pass # **replace** this line with your code

    # create matrix to record the cost matrix
    matrix = [[-1 for i in range(len(x))] for j in range(b)]
    # record the binning path list
    list_matrix = [[0 for i in range(len(x))] for j in range(b)]
    # record the best result
    best_matrix_list = [[0 for i in range(len(x))] for j in range(b)]
    # print(matrix)
    for i in range(1, b + 1):
        for j in range(len(x)):
            # the number of left bins should less than the number of previous element
            # && the number of right bins should less than the number of element rest
            if (b - i) <= j and i <= (len(x) - j):
                curr_list = x[j:]
                curr_bin = i
                # record first cost
                if i == 1:
                    cost = get_sse(curr_list)
                    matrix[i - 1][j] = cost
                    list_matrix[i - 1][j] = [curr_list]
                    best_matrix_list[i - 1][j] = [curr_list]
                else:
                    # print('i:',i)
                    # print('j:',j)
                    currcostL = []
                    pathL = []
                    if len(curr_list) == i:
                        min_cost = 0
                        for e in curr_list:
                            pathL.append([e])
                    # print(pathL)
                    else:
                        for h in range(1, len(curr_list) - i + 2):
                            prefix = curr_list[:h]
                            suffix = curr_list[h:]
                            pre_cost = get_sse(prefix)
                            # serch the previous result as index
                            index = list_matrix[i - 2].index([suffix])
                            # print('index:',index)
                            suf_path = best_matrix_list[i - 2][index]
                            suf_cost = matrix[i - 2][index]

                            cost = pre_cost + suf_cost
                            currcostL.append(cost)
                            # print('currcostL:',currcostL)

                            curr_path = []
                            curr_path.append(prefix)
                            for m in suf_path:
                                curr_path.append(m)
                            # print('curr_path:',curr_path)
                            pathL.append(curr_path)
                        # select the best result(min cost) to put in the matrix
                        min_cost = min(currcostL)
                        # put the min cost list into the best_matrix_list
                        min_cost_index = currcostL.index(min_cost)
                        pathL = pathL[min_cost_index]
                    # record the best list into best_matrix_list
                    best_matrix_list[i - 1][j] = pathL
                    matrix[i - 1][j] = min_cost
                    list_matrix[i - 1][j] = [curr_list]
    # for i in best_matrix_list:
    #    print(i)
    # in the record of the best_matrix_list,
    # the last list of the first element is the bins required
    bins = best_matrix_list[-1][0]
    return matrix, bins


matrix, bins = v_opt_dp(x, num_bins)
for i in matrix:
    print(i)
print(bins)


def v_opt_dp2(x, b, matrix, index_matrix, x_leave, bin_empty):
    if (len(x) - x_leave) > bin_empty and (b - bin_empty) > (len(x) - x_leave):
        v_opt_dp2(x, b, matrix, index_matrix, x_leave + 1, bin_empty)
        if (bin_empty == 0):
            matrix[bin_empty][x_leave] = np.var(x[x_leave:]) * len(x[x_leave:])
            return
    else:
        rest_list = x[x_leave:]


def v_opt_dp1(x, b):
    # record the best cost
    matrix = [[-1 for i in range(len(x))] for j in range(b)]
    # record index
    index_matrix = [[-1 for i in range(len(x))] for j in range(b)]

    x_leave = 0
    bin_empty = b - 1
    v_opt_dp2(x, b, matrix, index_matrix, x_leave, bin_empty)
    for i in range(b):


