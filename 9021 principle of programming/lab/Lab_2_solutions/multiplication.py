# Written by Eric Martin for COMP9021


'''
Decodes all multiplications of the form

                       *  *  *       ---x
                  x       *  *       ---y
                    ----------
                    *  *  *  *       ---product0
                    *  *  *          ---product1
                    ----------
                    *  *  *  *       ---total

such that the sum of all digits in all 4 columns is constant.
'''


for x in range(100, 1_000):
    for y in range(10, 100):
        product0 = x * (y % 10)
        #print('product0',product0)
        if product0 < 1_000:
            continue
        product1 = x * (y // 10)
        #print('product1',product1)
        if product1 >= 1_000:
            continue
        total = product0 + 10 * product1
        #print('total',total)
        if total >= 10_000:
            continue
        the_sum = x % 10 + y % 10 + product0 % 10 + total % 10
        if x // 10 % 10 + y // 10 + product0 // 10 % 10 + product1 % 10 + total // 10 % 10 !=\
                                                                                            the_sum:
            continue
        if x // 100 + product0 // 100 % 10 + product1 // 10 % 10 + total // 100 % 10 != the_sum:
            continue
        if product0 // 1_000 + product1 // 100 + total // 1_000 == the_sum:
            print(f'{x} * {y} = {total}, all columns adding up to {the_sum}.')



# 意思是 个位，是为，百位，千位 加起来 都一样
z=411 * 3
print(z)
z=411*10
print(z)
