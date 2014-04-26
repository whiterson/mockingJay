__author__ = 'Nathan'

import random


def uniform_variable(mean, spread):
    base = random.randrange(0, 2*spread) - spread
    s = base + mean
    return s


def discrete_variable(pmf, domain):
    cum_sum = 0
    cdf = [0]
    for x in range(domain[0], domain[1]):
        cum_sum += pmf(x)
        cdf.append(cum_sum)

    if cum_sum != 1:
        print 'Invalid pmf given to discrete_variable'

    num = random.random()
    index = 0
    while num > cdf[index]:
        index += 1

    return domain[0] + index
