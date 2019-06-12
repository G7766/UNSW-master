#Mean, median, and standard deviation

from random import seed, randint
from math import sqrt
from statistics import mean, median, pstdev
import sys


# Prompt the user for a seed for the random number generator,
# and for a strictly positive number, nb_of_elements.
#
# See previous challenge.


# Generate a list of nb_of_elements random integers between -50 and 50.
#
# See previous challenge.


# Print out the list, compute the mean, standard deviation and median of the list,
# and print them out.
#
# To compute the mean, use the builtin sum() function.
# To compute the standard deviation, use sum(), the sqrt() from the math module,
# and the ** operator (exponentiation).
# To compute the median, first sort the list.
#
# The following interaction at the python prompt gives an idea of how these functions work:
# >>> from math import sqrt
# >>> sqrt(16)
# 4.0
# >>> L = [2, 1, 3, 4, 0, 5]
# >>> L.sort()
# >>> L
# [0, 1, 2, 3, 4, 5]
# >>> L = [2, 1, 3, 4, 0, 5]
# >>> sum(L)
# 15
# >>> sum(x ** 2 for x in L)
# 55
# >>> L.sort()
# >>> L
# [0, 1, 2, 3, 4, 5]
#
# Then use the imported functions from the statistics module to check the results.

    