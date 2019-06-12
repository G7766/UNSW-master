import numpy as np

def v_opt_dp(x, b):  # do not change the heading of the function

    mtx = [[-1 for i in range(len(x))] for j in range(b)]
    dp_index = [[-1 for i in range(len(x))] for j in range(b)]

    # bin 0-3
    my_opt_dp(0, b - 1, x, b, mtx, dp_index)

    start = dp_index[-1][0]
    pre_start = start
    bins = [x[:start]]
    for i in range(len(dp_index) - 2, 0, -1):
        start = dp_index[i][start]
        bins.append(x[pre_start:start])
        pre_start = start
    bins.append(x[pre_start:])
    return mtx, bins


def my_opt_dp(mtx_x, remain_bins, x, b, mtx, dp_index):
    if (b - remain_bins - mtx_x < 2) and (len(x) - mtx_x > remain_bins):
        my_opt_dp(mtx_x + 1, remain_bins, x, b, mtx, dp_index)
        if (remain_bins == 0):
            mtx[remain_bins][mtx_x] = np.var(x[mtx_x:]) * len(x[mtx_x:])
            return
        my_opt_dp(mtx_x, remain_bins - 1, x, b, mtx, dp_index)
        mtx_l = [mtx[remain_bins - 1][mtx_x + 1]]
        mtx_l.extend( [mtx[remain_bins - 1][i] + (i - mtx_x) * np.var(x[mtx_x:i]) for i in range(mtx_x + 2, len(x))])
        # print(mtx_l)
        mtx[remain_bins][mtx_x] = min(mtx_l)
        dp_index[remain_bins][mtx_x] = mtx_l.index(min(mtx_l)) + mtx_x + 1



l = [3, 1, 18, 11, 13, 17]
bins = 4

m,b = v_opt_dp(l,bins)
for i in m:
    print(i)
print(b)

for i in range(2):
    print(i)
print('')
for  i in range(5,0,-1):
    print(i)

k = l[3:]
print(k)


index_matrix = [[None] for j in range(4)]
print(index_matrix)
print(l[5:])