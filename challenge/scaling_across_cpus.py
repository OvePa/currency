import random

mylist = [random.randint(1, 100000000) for i in range(1000000)]
# print(mylist)


def calc_min(li):
    minimum = li[0]
    for x in li:
        if x < minimum:
            minimum = x
    return minimum


print(calc_min(mylist))
